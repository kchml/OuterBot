import requests
from bs4 import BeautifulSoup
from lxml import html as lh
from ds_token import api_save, chrome_path
from geocoder import geocoder
from selenium import webdriver

def weather_scraper(city):

    coords = geocoder(city)
    key = api_save()
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={coords[0]}&lon={coords[1]}&appid={key}&units=metric"
    head = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.75"}
    response = requests.get(url, headers=head).json()
    temp = response['main']['temp']

    return temp

def selenium_scraper():

    pass
