# owm_reader.py
import requests
import json

api_token = '27ea49448c5aa859ddb9178e97e36ab1'
api_base_url = 'https://api.openweathermap.org/data/2.5/'
headers = {'Content-Type': 'application/json'}


def get_conditions(lat, lng):
    api_url = '{0}weather?lat={1}&lon={2}&appid={3}'.format(api_base_url, lat, lng, api_token)
    return get_json_response(api_url)


def get_json_response(url):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
