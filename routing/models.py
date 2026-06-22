from django.db import models

class Caseta(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=10, decimal_places=7)
    longitud = models.DecimalField(max_digits=10, decimal_places=7)
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'casetas'

class ZonaRoja(models.Model):
    nombre = models.CharField(max_length=100)
    nivel_riesgo = models.IntegerField()
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    class Meta:
        db_table = 'zonas_rojas'