from bs4 import BeautifulSoup
from urllib import urlencode
import requests

captcha_filepath = 'static/img/captcha.jpg'

image_base_url = 'http://google.com/sorry/image'

def store_captcha(s, html):
    soup = BeautifulSoup(html, 'html.parser')
    idd = soup.input.input['value']

    captcha_url = image_base_url + '?' + build_image_url_params(idd)
    img = s.get(captcha_url)

    f = open(captcha_filepath, 'w')
    f.write(img.content)
    f.close()

    return {
        'idd': idd,
        'img': captcha_filepath
    }

def build_image_url_params(idd):
    return urlencode({
        'id': idd,
        'hl': 'en'
    })
