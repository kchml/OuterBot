from ds_token import api_save
import requests

def geocoder(city):
    api_key = api_save()
    api_call = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"

    head = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.75"}
    response = requests.get(api_call, headers=head).json()

    lat = response[0]['lat']
    lon = response[0]['lon']

    return lat, lon