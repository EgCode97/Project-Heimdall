from django.shortcuts import render
import django.http as http

from rest_framework.views import APIView

from .influxDB import InfluxDB

def read(request):
    influx = InfluxDB.Client()
    # influx = Influx()
    influx.write(bucket="PRUEBA", measurement="headquarters", tagname="recepcion", tagvalue="piso_1", fields={"temperatura":23.50, "humedad":35} )
    return http.HttpResponse("done")


class Influx(APIView):
    def get(request):
        pass

    def post(request):
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