import requests
import psycopg2
import xml.etree.ElementTree as ET
import logging
import time
from datetime import datetime


logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)

reqUrl = "https://api.met.no/weatherapi/locationforecast/2.0/classic?lat=53.34&lon=-6.54&altitude=90"
city = "Celbridge"
locationEndPoint = './product/time/location/'

# headersList = {
#     "Accept": "*/*",
#     "User-Agent": "Thunder Client (https://www.thunderclient.com)"
# }

headersList = {}

payload = ""

HOST = ""
PORT = ""
DATABASE = ""
DBUSER = ""
DBPASSWORD = ""

def getComponent(name, endPoint, keyword):
    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    tree = ET.fromstring(response.text)
    result=tree.find(endPoint+f'{name}')
    
    return result.attrib[f'{keyword}']

while True:
    try:
        temperature = getComponent('temperature', locationEndPoint, 'value')
        windSpeed = getComponent('windSpeed', locationEndPoint, 'mps')
        humidity = getComponent('humidity', locationEndPoint, 'value')
        pressure = getComponent('pressure', locationEndPoint, 'value')
        fog = getComponent('fog', locationEndPoint, 'percent')
        precipitation = getComponent('precipitation', locationEndPoint, 'value')
        symbol = getComponent('symbol', locationEndPoint, 'code')

        if symbol.lower() == "rain" or symbol.lower() == "drizzle":
            rain = 1
        else:
            rain = 0

        if symbol.lower() == "snow":
            snow = 1
        else:
            snow = 0

        if symbol.lower() == "sun":
            sun = 1
        else:
            sun = 0

        data = { 
            "temperature": temperature,
            "windSpeed": windSpeed,
            "humidity": humidity,
            "pressure": pressure,
            "fog": fog,
            "precipitation": precipitation,
            "isRain" : rain,
            "isSnow" : snow,
            "isSun" : sun,
            "city": city
        }

        logging.info(data)
        logging.info('data received ...')
    except:
        logging.error('no response from api ...')

    try:
        logging.info('connection to database ...')
        connection = psycopg2.connect(
            user=DBUSER, password=DBPASSWORD, host=HOST, port=PORT, database=DATABASE)
        cursor = connection.cursor()

        sql = "insert into readings (temperature, windspeed, humidity, pressure, fog, precipitation, is_rain, is_snow, is_sun, city, lastupdate) values ('" + str(data['temperature']) + "', '" + str(data['windSpeed']) + "', '" + str(
            data['humidity']) + "', '" + str(data['pressure']) + "', '" + str(data['fog']) + "', '" + str(data['precipitation']) + "', '" + str(data['isRain']) + "', '" + str(data['isSnow']) + "', '" + str(data['isSun']) + "', '" + str(data['city']) + "', '" + datetime.now().isoformat() + "')"

        logging.info('start ingestion ...')
        cursor.execute(sql)
        connection.commit()
        cursor.close()
        connection.close()
        logging.info('ingestion done ...')
    except:
        logging.error('no database connection ...')

    time.sleep(300)
