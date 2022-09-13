import requests
from bs4 import BeautifulSoup
from lxml import html as lh

def weather_scraper(city):
    url = f"https://www.google.com/search?q=weather+{city}"
    head = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.75"}
    response = requests.get(url, headers=head)

    if response.status_code != 200:
        return None

    tree = lh.fromstring(response.text)
    temp_xpath = '/html/body/div[8]/div/div[11]/div/div[2]/div[2]/div/div/div[1]/div/div/div/div/div[1]/div[1]/div/div[1]/span[1]'
    temperature = tree.xpath(temp_xpath)
    print(temperature[0].text)
    msg_out = temperature[0].text
    return msg_out
