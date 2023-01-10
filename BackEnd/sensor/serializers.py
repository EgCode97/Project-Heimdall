from rest_framework.serializers import ModelSerializer
from .models import Station, Sensor
from core.serializers import ClientSerializer

class StationSerializer(ModelSerializer):
    client = ClientSerializer()    

    class Meta:
        fields = '__all__'
        model = Station


class SensorSerializer(ModelSerializer):
    station = StationSerializer()
    
    class Meta:
        fields = '__all__'
        model = Sensor