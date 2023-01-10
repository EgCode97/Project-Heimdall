from django.contrib import admin
from .models import Sensor, Station

@admin.register(Station)
class AdminStation(admin.ModelAdmin):
    list_display  = ('id','name', 'client')
    readonly_fields = ('id',)
    model = Station


@admin.register(Sensor)
class AdminSensor(admin.ModelAdmin):
    list_display  = ('id','name', 'station', 'type')
    readonly_fields = ('id',)
    model = Sensor