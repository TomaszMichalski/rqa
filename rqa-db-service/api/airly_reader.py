# airly_reader.py
import requests
import json

api_token = 'M5U3gq0ghEyVO7hRntNkKKABL6Bwcd1l'
api_base_url = 'https://airapi.airly.eu/v2/'
headers = {'Content-Type': 'application/json',
           'apikey': '{0}'.format(api_token)}


def get_installation(installation_id):
    api_url = '{0}installations/{1}'.format(api_base_url, installation_id)
    return get_json_response(api_url)


def get_nearest_installations(lat, lng, *args, **kwargs):
    api_url = '{0}installations/nearest?lat={1}&lng={2}'.format(api_base_url, lat, lng)

    max_dist = kwargs.get('max_dist', None)
    max_res = kwargs.get('max_res', None)

    if max_dist is not None:
        api_url = '{0}&maxDistanceKM={1}'.format(api_url, max_dist)
    if max_res is not None:
        api_url = '{0}&maxResults={1}'.format(api_url, max_res)

    return get_json_response(api_url)


def get_measurements(installation_id):  # TODO: handle 301 (Moved Permanently)
    api_url = '{0}measurements/installation?installationId={1}'.format(api_base_url, installation_id)
    return get_json_response(api_url)


def get_nearest_measurements(lat, lng, *args, **kwargs):
    api_url = '{0}measurements/nearest?lat={1}&lng={2}'.format(api_base_url, lat, lng)

    max_dist = kwargs.get('max_dist', None)

    if max_dist is not None:
        api_url = '{0}&maxDistanceKM={1}'.format(api_url, max_dist)

    return get_json_response(api_url)


def get_point_measurements(lat, lng):
    api_url = '{0}measurements/point?lat={1}&lng={2}'.format(api_base_url, lat, lng)
    return get_json_response(api_url)


def get_json_response(url):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
