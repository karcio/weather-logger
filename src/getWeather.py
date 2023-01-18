import requests
import xml.etree.ElementTree as ET

reqUrl = "https://api.met.no/weatherapi/locationforecast/2.0/classic?lat=53.34&lon=-6.54&altitude=90"

headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)"
}

payload = ""

response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
tree = ET.fromstring(response.text)

temperature = tree.find('./product/time/location/temperature')
print(temperature.attrib)

windSpeed = tree.find('./product/time/location/windSpeed')
print(windSpeed.attrib)

humidity = tree.find('./product/time/location/humidity')
print(humidity.attrib)

pressure = tree.find('./product/time/location/pressure')
print(pressure.attrib)

fog = tree.find('./product/time/location/fog')
print(fog.attrib)

precipitation = tree.find('./product/time/location/precipitation')
print(precipitation.attrib)

forecast = tree.find('./product/time/location/symbol')
print(forecast.attrib)