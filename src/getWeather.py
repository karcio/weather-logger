import requests
import xml.etree.ElementTree as ET

reqUrl = "https://api.met.no/weatherapi/locationforecast/2.0/classic?lat=53.34&lon=-6.54&altitude=90"
locationEndPoint = './product/time/location/'

# headersList = {
#     "Accept": "*/*",
#     "User-Agent": "Thunder Client (https://www.thunderclient.com)"
# }

headersList = {}

payload = ""

def getComponent(name, endPoint, keyword):
    response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
    tree = ET.fromstring(response.text)
    result=tree.find(endPoint+f'{name}')
    print(result.attrib[f'{keyword}'])

# getComponent('temperature', locationEndPoint, 'value')
# getComponent('windSpeed', locationEndPoint, 'mps')
# getComponent('humidity', locationEndPoint, 'value')
# getComponent('pressure', locationEndPoint, 'value')
# getComponent('fog', locationEndPoint, 'percent')
# getComponent('precipitation', locationEndPoint, 'value')
# getComponent('symbol', locationEndPoint, 'code')
