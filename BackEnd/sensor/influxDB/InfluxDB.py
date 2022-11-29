import influxdb_client, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from decouple import config

# token = config("INFLUXDB_TOKEN")
# org = "Heimdall"
# url = "192.168.0.107:8086"

# client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

# bucket="PRUEBA"

class Client:
    def __init__(self) -> None:
        self.url = "192.168.0.107:8086"
        self.org = "Heimdall"
        self.client = influxdb_client.InfluxDBClient(url=self.url, token=config("INFLUXDB_TOKEN"), org=self.org)

    def write(self, bucket:str=None, measurement:str=None, tagname:str=None, tagvalue:str=None, fields:dict=None):
        '''Write data to influxDB indicating the following:
        * bucket: the bucket name where the measurements are stored
        * measurement: the measurement name where where the time series are grouped
        * tagname: the tag name associated with the current data
        * tagvalue: the tag value associated with the current data
        * fields: a dictionary containing the metrics to be stored where the dict key represents the field name and the dict value represents the value to be stored
        
        Eg: write( bucket="office", measurement="headquarters", tagname="recepcion", tagvalue="piso_1", fields={"temperatura":23.50, "humedad":35} )
        '''

        write_api = self.client.write_api(write_options=SYNCHRONOUS)
        point = Point(measurement).tag(tagname, tagvalue)
        for field in fields:
            point.field(field, fields[field])
        
        write_api.write(bucket=bucket, org="Heimdall", record=point)


        





    def read(self):
        query_api = self.client.query_api()

        query = """from(bucket: "PRUEBA")
        |> range(start: -10d)
        |> filter(fn: (r) => r._measurement == "measurement1")"""
        tables = query_api.query(query, org="Heimdall")

        for table in tables:
            print(table)
            for record in table.records:
                print(record)
        
