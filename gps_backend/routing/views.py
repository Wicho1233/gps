from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .utils import (
    geocode_address, reverse_geocode, get_osrm_routes,
    manhattan_distance_meters, get_casetas, get_zonas_rojas,
    route_passes_near_zone, calculate_toll_cost, point_to_line_distance
)
from .models import ZonaRoja, Caseta  # Importar Caseta

VEHICLE_CONSUMPTION = {
    'carro': 12,
    'autobus': 5,
    'carga': 4,
}

@csrf_exempt
@require_http_methods(["POST"])
def route_api(request):
    try:
        data = json.loads(request.body)
        origin_lat = data.get('origin_lat')
        origin_lng = data.get('origin_lng')
        dest_address = data.get('destination')
        dest_lat = data.get('dest_lat')
        dest_lng = data.get('dest_lng')
        fuel_liters = float(data.get('fuel', 0))
        vehicle_type = data.get('vehicle_type', 'carro')
        consumption = float(data.get('consumption', VEHICLE_CONSUMPTION.get(vehicle_type, 10)))

        if not all([origin_lat, origin_lng]):
            return JsonResponse({'error': 'Falta origen'}, status=400)

        # Geocodificar destino
        if dest_lat is not None and dest_lng is not None:
            dest_address = reverse_geocode(dest_lat, dest_lng) or f"({dest_lat}, {dest_lng})"
        elif dest_address:
            dest_lat, dest_lng = geocode_address(dest_address)
            if dest_lat is None:
                return JsonResponse({'error': 'No se pudo geocodificar la dirección'}, status=404)
        else:
            return JsonResponse({'error': 'Falta destino'}, status=400)

        # Obtener rutas (hasta 3)
        routes = get_osrm_routes(origin_lat, origin_lng, dest_lat, dest_lng)
        if not routes:
            return JsonResponse({'error': 'No se pudo calcular la ruta'}, status=500)

        # Cargar datos de BD
        casetas = get_casetas()
        zonas = get_zonas_rojas()

        autonomy_m = fuel_liters * consumption * 1000

        # Evaluar cada ruta
        evaluated = []
        for route in routes:
            coords = route['geometry']['coordinates']
            zona_nombre, dist_zone = route_passes_near_zone(coords, zonas, threshold_km=1.0)
            toll_cost = calculate_toll_cost(coords, casetas, threshold_km=0.5)
            dist_m = route['distance']
            evaluated.append({
                'route': route,
                'coords': coords,
                'distance': dist_m,
                'duration': route['duration'],
                'zona_peligrosa': zona_nombre is not None,
                'zona_nombre': zona_nombre,
                'zona_dist': dist_zone,
                'toll_cost': toll_cost,
                'fuel_needed': dist_m / 1000 / consumption,
            })

        # Filtrar por autonomía
        feasible = [r for r in evaluated if r['distance'] <= autonomy_m or fuel_liters == 0]
        if not feasible:
            feasible = evaluated

        # Preferir rutas seguras
        safe = [r for r in feasible if not r['zona_peligrosa']]
        if safe:
            best = min(safe, key=lambda r: (r['distance'], r['toll_cost']))
        else:
            best = min(feasible, key=lambda r: (r['zona_dist'] if r['zona_peligrosa'] else 0, r['distance']))

        fuel_sufficient = best['distance'] <= autonomy_m or fuel_liters == 0

        # Obtener casetas cercanas a la ruta seleccionada (para devolver al frontend)
        casetas_cercanas = []
        for c in casetas:
            c_lat = float(c['latitud'])
            c_lon = float(c['longitud'])
            dist = point_to_line_distance(c_lon, c_lat, best['coords'])
            if dist < 500:  # 500 metros
                casetas_cercanas.append({
                    'nombre': c['nombre'],
                    'latitud': c_lat,
                    'longitud': c_lon,
                    'costo': float(c['costo'])
                })

        # Distancia Manhattan
        manhattan_dist = manhattan_distance_meters(origin_lat, origin_lng, dest_lat, dest_lng)

        return JsonResponse({
            'origin': {'lat': origin_lat, 'lng': origin_lng},
            'destination': {'lat': dest_lat, 'lng': dest_lng},
            'destination_address': dest_address,
            'geometry': best['route']['geometry'],
            'steps': best['route']['steps'],
            'distance_real': best['distance'],
            'duration_real': best['duration'],
            'distance_manhattan': manhattan_dist,
            'fuel_sufficient': fuel_sufficient,
            'fuel_needed': round(best['fuel_needed'], 2),
            'fuel_available': fuel_liters,
            'autonomy': round(autonomy_m / 1000, 2),
            'toll_cost': round(best['toll_cost'], 2),
            'zona_peligrosa': best['zona_peligrosa'],
            'zona_nombre': best['zona_nombre'],
            'zona_dist': round(best['zona_dist'], 2) if best['zona_dist'] else None,
            'casetas': casetas_cercanas,
            'vehicle_type': vehicle_type,
            'consumption': consumption,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ===== VISTA PARA ZONAS ROJAS =====
def zonas_rojas_api(request):
    """Devuelve todas las zonas rojas con coordenadas."""
    zonas = ZonaRoja.objects.exclude(latitud__isnull=True).exclude(longitud__isnull=True).values('nombre', 'latitud', 'longitud', 'nivel_riesgo')
    return JsonResponse(list(zonas), safe=False)

# ===== NUEVAS VISTAS PARA CASETAS =====
def listar_casetas(request):
    """Devuelve todas las casetas registradas en la base de datos."""
    casetas = Caseta.objects.all().values('id', 'nombre', 'latitud', 'longitud', 'costo')
    return JsonResponse(list(casetas), safe=False)

def casetas_cercanas(request):
    """
    Devuelve las casetas que están dentro de un radio (en km) de una coordenada dada.
    Parámetros GET:
        - lat: latitud (requerido)
        - lng: longitud (requerido)
        - radio: radio en km (opcional, por defecto 10)
    """
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    radio_km = request.GET.get('radio', 10)

    if not lat or not lng:
        return JsonResponse({'error': 'Faltan parámetros lat y lng'}, status=400)

    try:
        lat = float(lat)
        lng = float(lng)
        radio_km = float(radio_km)
    except ValueError:
        return JsonResponse({'error': 'Parámetros inválidos'}, status=400)

    # Aproximación: 1 grado ≈ 111 km
    delta = radio_km / 111.0

    casetas = Caseta.objects.filter(
        latitud__gte=lat - delta,
        latitud__lte=lat + delta,
        longitud__gte=lng - delta,
        longitud__lte=lng + delta
    ).values('id', 'nombre', 'latitud', 'longitud', 'costo')

    return JsonResponse(list(casetas), safe=False)