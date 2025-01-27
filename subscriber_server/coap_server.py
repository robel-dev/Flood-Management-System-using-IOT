import datetime
import logging
logging.basicConfig(level=logging.WARNING)
logging.getLogger("coap-server").setLevel(logging.WARNING)
import asyncio
import aiocoap.resource as resource
import aiocoap
import csv

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
token_="GtEeLWZqA42o88CVxUQg2dvBqTduZuC-NXgBVMwqZX7pce1bWhmQzMEO8woGOpPdh1wWqWZBo4Jz0U-JhpxHnQ=="
org_="anelyamend@gmail.com"
url_="https://us-east-1-1.aws.cloud2.influxdata.com"

# token_ = 'skVO0ckLCISprVeTI43CrtXCk1NSoJmlGQlN_X1FfpzOJ48c5JTatF4Tb3p-sRYtkaJ52vjFKCqcI5wrrpqGAg=='
# org_ = "robelamare20@gmail.com"
# url_ = "https://eu-central-1-1.aws.cloud2.influxdata.com"


client = influxdb_client.InfluxDBClient(url=url_, token=token_, org=org_)

measurements = ['humidity', 'temperature']
data = [
    {
"measurement": measurements[0],"tags": {"host": "server01"},"fields": {"value": 100}},
{
"measurement": measurements[1],"tags": {"host": "server01"},"fields": {"value": 100}},
]
bucket1 = 'indus'
bucket2 = 'jehlum'
write_api = client.write_api(write_options=SYNCHRONOUS)


f = open('C:/Users/Tasbiha/Iot/rawdata.csv', 'w', newline='')
writer = csv.writer(f)

def collect_data(pay, r):
    arr = r.split("_")
    sen_name = arr[1] + "_" + arr[2]
    point = (
        Point(arr[1])
        .tag("sensor name", sen_name)
        .field("value", float(pay))
    )
    # point = (
    #     Point(arr[0])
    #     .tag("location", arr[2])
    #     .field(arr[1], )
    # )
    # print(point)
    '''FOR INDUS'''
    if arr[0] == "Indus":
        write_api.write(bucket=bucket1, org=org_, record=point)
    '''FOR JEHLUM'''
    if arr[0] == "Jehlum":
        write_api.write(bucket=bucket2, org=org_, record=point)
class Humidity(resource.Resource):

    def __init__(self, name):
        self.name = name

    async def render_post(self, request):
        payload = request.payload.decode("ascii")
        writer.writerow((self.name, payload))
        #print("Received message: ", payload, "from", self.name)
        collect_data(payload, self.name)
        return  #aiocoap.Message(code=CHANGED, payload=b"ACK")

class Temperature(resource.Resource):
    def __init__(self, name):
        self.name = name

    async def render_post(self, request):
        payload = request.payload.decode("ascii")
        writer.writerow((self.name, payload))
        #print("Received message: ", payload, "from", self.name)
        collect_data(payload, self.name)
        return #aiocoap.Message(code=CHANGED, payload=b"ACK")

# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
    # Resource tree creation
    root = resource.Site()

    root.add_resource(('Indus_humidity_sensor1',), Humidity('Indus_humidity_sensor1'))
    root.add_resource(('Indus_humidity_sensor2',), Humidity('Indus_humidity_sensor2'))
    root.add_resource(('Indus_temperature_sensor1',), Temperature('Indus_temperature_sensor1'))
    root.add_resource(('Indus_temperature_sensor2',), Temperature('Indus_temperature_sensor2'))

    root.add_resource(('Jehlum_humidity_sensor1',), Humidity('Jehlum_humidity_sensor1'))
    root.add_resource(('Jehlum_humidity_sensor2',), Humidity('Jehlum_humidity_sensor2'))
    root.add_resource(('Jehlum_temperature_sensor1',), Temperature('Jehlum_temperature_sensor1'))
    root.add_resource(('Jehlum_temperature_sensor2',), Temperature('Jehlum_temperature_sensor2'))


    await aiocoap.Context.create_server_context(root, bind = ('localhost', 5683))

    # Run forever
    await asyncio.get_running_loop().create_future()
    # close the file
    f.close()



if __name__ == "__main__":
    asyncio.run(main())
