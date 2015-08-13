from flask import g
from bs4 import BeautifulSoup
from urllib import urlencode
import sqlite3
import requests
import os
import errno

insert_query = 'INSERT INTO sounds (lang, text, path) values (?, ?, ?)'

select_path_query = 'SELECT * FROM sounds WHERE path = ?'

select_idd_query = 'SELECT * FROM sounds WHERE id = ?'

# returns id of new sound
def insert_sound(lang, text, path):
    cur = g.db.execute(insert_query, [lang, text, path])
    g.db.commit()

    sound = get_sound_by_path(path)
    return sound[0]

def get_sound_by_path(path):
    cur = g.db.execute(select_path_query, [path])
    res = cur.fetchone()
    return res

def get_sound_by_id(idd):
    cur = g.db.execute(select_idd_query, [idd])
    res = cur.fetchone()
    return res

sound_path = 'static/sounds/%(lang)s/%(text)s.mp3'

captcha_filepath = 'static/img/captcha.jpg'

image_base_url = 'http://google.com/sorry/image'

def save_sound(lang, text, sound):
    pathText = "".join( map(to_file_path, text) )
    path = sound_path % { 'lang': lang, 'text': pathText }

    create_dir_if_not_exists('static/sounds/' + lang)

    f = open(path, 'w')
    f.write(sound)
    f.close()

    return path

def to_file_path(c):
    switcher = {
        ' ': '_',
        '/': '-',
    }
    return switcher.get(c, c)

def create_dir_if_not_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

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