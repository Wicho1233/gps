import requests
import math
from django.db import connection
from .models import Caseta, ZonaRoja

# Constantes para conversión de grados a metros
METROS_POR_GRADO_LAT = 111320
METROS_POR_GRADO_LON = 111320 * math.cos(math.radians(40.7))

def geocode_address(address):
    """Geocodifica una dirección a (lat, lon) usando Nominatim."""
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': address, 'format': 'json', 'limit': 1}
    headers = {'User-Agent': 'ManhattanGPS/1.0'}
    resp = requests.get(url, params=params, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    return None, None

def reverse_geocode(lat, lon):
    """Obtiene dirección a partir de coordenadas."""
    url = 'https://nominatim.openstreetmap.org/reverse'
    params = {'lat': lat, 'lon': lon, 'format': 'json', 'zoom': 18}
    headers = {'User-Agent': 'ManhattanGPS/1.0'}
    resp = requests.get(url, params=params, headers=headers)
    if resp.status_code == 200:
        data = resp.json()
        if 'display_name' in data:
            return data['display_name']
    return None

def get_osrm_routes(origin_lat, origin_lon, dest_lat, dest_lon):
    """
    Obtiene hasta 3 rutas alternativas de OSRM.
    Devuelve una lista de rutas, cada una con geometry, steps, distance, duration.
    """
    coords = f"{origin_lon},{origin_lat};{dest_lon},{dest_lat}"
    url = f"http://router.project-osrm.org/route/v1/driving/{coords}"
    params = {
        'overview': 'full',
        'geometries': 'geojson',
        'steps': 'true',
        'alternatives': 'true'
    }
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data.get('code') == 'Ok' and 'routes' in data:
            routes = []
            for route in data['routes']:
                steps = []
                for leg in route['legs']:
                    for step in leg['steps']:
                        steps.append({
                            'instruction': step.get('maneuver', {}).get('instruction', ''),
                            'distance': step.get('distance', 0),
                            'duration': step.get('duration', 0),
                        })
                routes.append({
                    'geometry': route['geometry'],
                    'steps': steps,
                    'distance': route['distance'],
                    'duration': route['duration'],
                })
            return routes
    return []

def manhattan_distance_meters(lat1, lon1, lat2, lon2):
    dx = abs(lon2 - lon1) * METROS_POR_GRADO_LON
    dy = abs(lat2 - lat1) * METROS_POR_GRADO_LAT
    return dx + dy

def get_casetas():
    return list(Caseta.objects.all().values('nombre', 'latitud', 'longitud', 'costo'))

def get_zonas_rojas():
    return list(ZonaRoja.objects.exclude(latitud__isnull=True).exclude(longitud__isnull=True).values('nombre', 'latitud', 'longitud', 'nivel_riesgo'))

def point_to_line_distance(px, py, line_coords):
    """
    Distancia en metros de un punto (px, py) a una polilínea (lista de [lng, lat])
    """
    min_dist = float('inf')
    for i in range(len(line_coords)-1):
        x1, y1 = line_coords[i]
        x2, y2 = line_coords[i+1]
        # Convertir a metros
        dx = (x2 - x1) * METROS_POR_GRADO_LON
        dy = (y2 - y1) * METROS_POR_GRADO_LAT
        # Proyección
        t = ((px - x1)*dx + (py - y1)*dy) / (dx*dx + dy*dy + 1e-10)
        t = max(0, min(1, t))
        proj_x = x1 + t*(x2-x1)
        proj_y = y1 + t*(y2-y1)
        dist = math.sqrt((px - proj_x)**2 * METROS_POR_GRADO_LON**2 + (py - proj_y)**2 * METROS_POR_GRADO_LAT**2)
        if dist < min_dist:
            min_dist = dist
    return min_dist

def route_passes_near_zone(route_coords, zones, threshold_km=1.0):
    """Verifica si la ruta pasa cerca de alguna zona roja (threshold en km)"""
    for zone in zones:
        z_lat = float(zone['latitud'])
        z_lon = float(zone['longitud'])
        dist = point_to_line_distance(z_lon, z_lat, route_coords)
        if dist < threshold_km * 1000:
            return zone['nombre'], dist
    return None, None

def calculate_toll_cost(route_coords, casetas, threshold_km=0.5):
    """Suma el costo de casetas que estén cerca de la ruta"""
    total = 0
    for caseta in casetas:
        c_lat = float(caseta['latitud'])
        c_lon = float(caseta['longitud'])
        dist = point_to_line_distance(c_lon, c_lat, route_coords)
        if dist < threshold_km * 1000:
            total += float(caseta['costo'])
    return total