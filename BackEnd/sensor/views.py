from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from rest_framework.views import APIView

from core.models import Client

from .influxDB import InfluxDB
from .models import Station, Sensor
from .serializers import StationSerializer, SensorSerializer


class Influx(APIView):
    '''
    This API takes the http request and use the "influxDB" module to query and write measeurements into the InfluxDB
    '''
    def get(self, request):
        json_data = dict()
        json_data['count'] = 0
        json_data['data'] = list()
        influx_client = InfluxDB.Client()
        query_params = request.query_params 

        tables = influx_client.read(
            bucket= query_params.get('bucket'),
            measurement= query_params.get('measurement'),
            tagname= query_params.get('tagname'),
            tagvalue= query_params.get('tagvalue'),
            fields= query_params.get('fields').split(';') if query_params.get('fields') else None,
            range= query_params.get('range') if query_params.get('fields') else '-8h'
        )

        for table in tables:
            # print(table)
            for record in table.records:
                ret = record.values
                json_data['data'].append(record.values)
                print(record.values)
            #     break
            # break

        return JsonResponse(json_data)

    @csrf_exempt
    def post(self, request):
        data = request.data if request.data else request.POST
        if not (data.get('bucket'), data.get('measurement'), data.get('tag'), data.get('fields')):
            response = HttpResponse()
            response.status_code = 400
            return response

        influx_client = InfluxDB.Client()
        influx_client.write(
            bucket= data['bucket'],
            measurement= data['measurement'],
            tagname= data['tag']['tagname'],
            tagvalue= data['tag']['tagvalue'],
            fields= data['fields']
        )

        response = HttpResponse()
        response.status_code = 200

        return response



class SensorApi(APIView):
    '''
    API used to perform CRUD operations on the "Sensor" model.

    It can also handles this operations through http requests
    '''

    @staticmethod
    def create_sensor(name:str, station_id:int, sensor_type:str):
        sensor, error = None, None
        try:
            station = Station.objects.get(id=station_id)
        except Station.DoesNotExist:
            error = 'Station doesn\'t exists'
            return sensor, error

        if sensor_type not in [type[0] for type in Sensor.sensor_types]:
            error = 'Sensor type not supported'
            return sensor, error    

        elif name in [sensor.name for sensor in Sensor.objects.filter(station__id=station_id)]:
            error = 'Sensor name already exists for this station'
            return sensor, error

        sensor = Sensor.objects.create(
            name= name,
            station= station,
            type= sensor_type
        )

        return sensor, error


    @staticmethod
    def update_sensor(id:int, new_name:str=None, new_type:str=None):
        sensor, error = None, None
        try:
            sensor = Sensor.objects.get(id=id)
        except Sensor.DoesNotExist:
            error = 'Sensor doesn\t exists'
            return sensor, error
        
        if new_name in [sensor.name for sensor in Sensor.objects.filter(station__id=sensor.station.id)]:
            error = 'sensor name already in use for the station'
            return sensor, error
        
        elif new_type not in [sensor_tuple[0] for sensor_tuple in Sensor.sensor_types]:
            error = 'sensor type not supported'
            return sensor, error
        
        sensor.name = new_name if new_name else sensor.name
        sensor.type = new_type if new_type else sensor.type
        sensor.save()
        return sensor, error


    @staticmethod
    def search_sensor(id:int=None, name:str=None, station:int=None, type:str=None):
        if id:
            search = Sensor.objects.filter(id=id)
        
        elif name and station:
            search = Sensor.objects.filter(station__id=station, name=name)

        elif station and type:
            search = Sensor.objects.filter(station__id=station, type=type)
        
        elif station:
            search = Sensor.objects.filter(station__id=station)

        else:
            search = Sensor.objects.none()

        return search


    def get(self, request) -> JsonResponse:
        response = dict()
        query_params = request.GET.copy()
        
        search = SensorApi.search_sensor(
            id= query_params.get('id'),
            name= query_params.get('name'),
            station= query_params.get('station'),
            type= query_params.get('type')
        )
        response['data'] = SensorSerializer(search, many=True).data
        return JsonResponse(response)

    def post(self, request) -> JsonResponse:
        json_data = dict()
        json_data['success'] = False
        json_data['error'] = None
        json_data['data'] = None

        error = None
        params = request.data
        if 'name' in params and 'station' in params and 'type' in params:
            sensor, error = SensorApi.create_sensor(name=params['name'], station_id=params['station'], sensor_type=params['type'])
        else:
            error = 'invalid parameters'
        
        if not error:
            json_data['data'] = SensorSerializer(sensor).data

        else:
            json_data['error'] = error

        json_data['success'] = bool(json_data['data'])

        return JsonResponse(json_data)

    def put(self, request) -> JsonResponse:
        json_data = dict()
        json_data['success'] = False
        json_data['error'] = None
        json_data['data'] = None

        error = None
        params = request.data
        if 'id' in params:
            sensor, error = SensorApi.update_sensor(id=params['id'], new_name=params.get('name'), new_type=params.get('type'))
        else:
            error = 'invalid parameters'
        
        if not error:
            json_data['data'] = SensorSerializer(sensor).data

        else:
            json_data['error'] = error

        json_data['success'] = bool(json_data['data'])

        return JsonResponse(json_data)



class StationApi(APIView):
    '''
    API used to perform CRUD operations on the "Sensor" model.

    It can also handles this operations through http requests
    '''

    @staticmethod
    def create_station(name:str, client_id:int):
        station, error = None, None
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            error = 'Client doesn\'t exists'
            return station, error

        client_stations = [station.name.lower() for station in Station.objects.filter(client__id=client_id)]

        if name.lower() in client_stations:
            error = 'Station already exists for this client'
        else:
            station = Station.objects.create(name=name, client=client)
        
        return station, error 

    @staticmethod
    def update_station(new_name:str, id:int):
        station, error = None, None
        try:
            station = Station.objects.get(id=id)
        except Station.DoesNotExist:
            error = 'Station doesn\'t exists'
            return station, error

        client_stations = [station.name.lower() for station in Station.objects.filter(client__id=station.client.id)]

        if new_name.lower() in client_stations:
            error = 'Station already exists for this client'
        else:
            station.name = new_name
            station.save()
        
        return station, error 


    @staticmethod
    def search_station(id:int=None, client:int=None):
        if id:
            search = Station.objects.filter(id=id)

        elif client:
            search = Station.objects.filter(client__id=client)

        else:
            search = Station.objects.none()

        return search
                


    def get(self, request) -> JsonResponse:
        response = dict()
        query_params = request.GET.copy()
        
        search = StationApi.search_station(
            id= query_params.get('id'),
            client= query_params.get('client')
        )
        response['data'] = StationSerializer(search, many=True).data
        return JsonResponse(response)

    def post(self, request) -> JsonResponse:
        json_data = dict()
        json_data['success'] = False
        json_data['error'] = None
        json_data['data'] = None

        error = None
        params = request.data
        if 'name' in params and 'client' in params:
            station, error = StationApi.create_station(name=params['name'], client_id=params['client'])
        else:
            error = 'invalid parameters'
        
        if not error:
            json_data['data'] = StationSerializer(station).data

        else:
            json_data['error'] = error

        json_data['success'] = bool(json_data['data'])

        return JsonResponse(json_data)

    def put(self, request) -> JsonResponse:
        json_data = dict()
        json_data['success'] = False
        json_data['error'] = None
        json_data['data'] = None

        error = None
        params = request.data
        if 'name' in params and 'id' in params:
            station, error = StationApi.update_station(new_name=params['name'], id=params['id'])
        else:
            error = 'invalid parameters'
        
        if not error:
            json_data['data'] = StationSerializer(station).data

        else:
            json_data['error'] = error

        json_data['success'] = bool(json_data['data'])

        return JsonResponse(json_data)