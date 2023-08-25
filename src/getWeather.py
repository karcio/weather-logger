import requests
import psycopg2
import xml.etree.ElementTree as ET
import logging
import time
from datetime import datetime
import configparser


logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
                    level=logging.INFO)

config = configparser.ConfigParser()
config.read('config.ini')

db_config = config['database']
db_host = db_config['host']
db_port = db_config['port']
db_name = db_config['database']
db_username = db_config['username']
db_password = db_config['password']

url_config = config['url']
url_endpoint = url_config['endpoint']
url_long = url_config['long']
url_lat = url_config['lat']
url_alt = url_config['alt']

reqUrl = "https://" + url_endpoint + "lat=" + url_lat + "&lon=" \
    + url_long + "&altitude=" + url_alt + ""
city = "Celbridge"
locationEndPoint = './product/time/location/'
# headersList = {}
headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)"
}
payload = ""


def getComponent(name, endPoint, keyword):
    response = requests.request("GET", reqUrl, data=payload,
                                headers=headersList)
    tree = ET.fromstring(response.text)
    result = tree.find(endPoint+f'{name}')
    return result.attrib[f'{keyword}']


while True:
    try:
        temperature = getComponent('temperature', locationEndPoint, 'value')
        windSpeed = getComponent('windSpeed', locationEndPoint, 'mps')
        humidity = getComponent('humidity', locationEndPoint, 'value')
        pressure = getComponent('pressure', locationEndPoint, 'value')
        fog = getComponent('fog', locationEndPoint, 'percent')
        precipitation = getComponent('precipitation',
                                     locationEndPoint, 'value')
        symbol = getComponent('symbol', locationEndPoint, 'code')

        weather_mappings = {
            "rain": ["rain", "lightrain", "lightrainshowers_day",
                     "rainshowers_day", "heavyrain", "heavyrainshowers_day"],
            "snow": ["snow"],
            "sun": ["sun", "clearsky_day", "fair_day"]
        }

        symbol_lower = symbol.lower()

        rain = 1 if any(cond in symbol_lower for cond in weather_mappings["rain"]) else 0
        snow = 1 if any(cond in symbol_lower for cond in weather_mappings["snow"]) else 0
        sun = 1 if any(cond in symbol_lower for cond in weather_mappings["sun"]) else 0

        data = {
            "details": symbol,
            "temperature": temperature,
            "windSpeed": windSpeed,
            "humidity": humidity,
            "pressure": pressure,
            "fog": fog,
            "precipitation": precipitation,
            "isRain": rain,
            "isSnow": snow,
            "isSun": sun,
            "city": city
        }

        logging.info(data)
        logging.info('data received ...')
    except Exception as e:
        logging.error(e)
        logging.error('no response from api ...')

    try:
        logging.info('connection to database ...')
        connection = psycopg2.connect(
            user=db_username, password=db_password, host=db_host, port=db_port,
            database=db_name)
        cursor = connection.cursor()

        sql = """
                INSERT INTO readings
                    (details, temperature, windspeed, humidity, pressure,
                    fog, precipitation, is_rain, is_snow, is_sun,
                    city, lastupdate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

        values = (
            data['details'],
            data['temperature'],
            data['windSpeed'],
            data['humidity'],
            data['pressure'],
            data['fog'],
            data['precipitation'],
            data['isRain'],
            data['isSnow'],
            data['isSun'],
            data['city'],
            datetime.now().isoformat(),
        )

        logging.info('start ingestion ...')
        cursor.execute(sql, values)
        connection.commit()
        cursor.close()
        connection.close()
        logging.info('ingestion done ...')
    except Exception as e:
        logging.error(e)
        logging.error('no database connection ...')

    time.sleep(300)
