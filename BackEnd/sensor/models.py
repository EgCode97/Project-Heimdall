from django.db import models
from core.models import Client

class Station(models.Model):
    name = models.CharField(max_length=100, db_column='SnrStnNme')
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE, db_column='SnsStnCliID')

    class Meta:
        db_table= 'SnrStn'

    def __str__(self) -> str:
        return self.name

class Sensor(models.Model):
    sensor_types = [
        ('T', 'Temperatura'),
    ] 
    name = models.CharField(max_length=100, db_column='SnrSnrNme')
    station = models.ForeignKey(to=Station, on_delete=models.CASCADE, db_column='SnrSnrStnID')
    type = models.CharField(max_length=3, choices=sensor_types, db_column='SnrSnrTpe')

    class Meta:
        db_table= 'SnrSnr'

    def __str__(self) -> str:
        return self.name