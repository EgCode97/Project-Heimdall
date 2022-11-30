from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import django.http as http

from rest_framework.views import APIView

from .influxDB import InfluxDB


class Influx(APIView):
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

        return http.JsonResponse(json_data)

    @csrf_exempt
    def post(self, request):
        data = request.data if request.data else request.POST
        if not (data.get('bucket'), data.get('measurement'), data.get('tag'), data.get('fields')):
            response = http.HttpResponse()
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

        return http.HttpResponse('ok')