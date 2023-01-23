'''For the temperature of city of Qambar'''
# client_put.py
import asyncio
import random
import requests
import logging
import pandas as pd
from aiocoap import *
import datetime
import aiocoap.resource as resource
import aiocoap



link = "http://www.wapda.gov.pk/index.php/river-flow-data"
dfs = pd.read_html(link, header=None, skiprows=4, index_col=None)

Indus_date = dfs[0][0]


class Resource(resource.Resource):
    """This resource supports the PUT method.
    PUT: Update state of alarm."""

    def __init__(self):
        super().__init__()
        self.state = ""

    async def render_put(self, request):
        self.state = request.payload
        print('Received Temperature: %s' % self.state)

        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.state)


logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
    # Resource tree creation
    context = await Context.create_client_context()
    for i in Indus_date:
        i = str(i)
        month = i[len(i)-3] + i[len(i)-2] + i[len(i)-1]
        if month == 'Nov' or month == 'Dec' or month == 'Jan' or month == 'Feb':
            temp = random.randint(37, 50)
        if month == 'March' or month == 'April' or month == 'May':
            temp = random.randint(33, 40)
        if month == 'June' or month == 'July' or month == 'August':
            temp = random.randint(34, 57)
        if month == 'Sep' or month == 'Oct' or month == 'Nov':
            temp = random.randint(42, 54)
        data = "{}".format(temp)
        request = Message(code=POST, payload=data.encode("ascii"),
                          uri='coap://localhost:5683/humidity_sensor2_jehlum')
        try:
            response = await context.request(request).response
            # print(response)
        except Exception as e:
            print('Failed to send data:')
            print(e)
        else:
            print('Sent data:', data)
            print('Received ACK:', response.payload.decode("ascii"))
        #await asyncio.sleep(2)

asyncio.get_event_loop().run_until_complete(main())
