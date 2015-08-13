from flask import request, jsonify, render_template
from urllib import urlencode
from captcha import store_captcha
import requests
import os
import errno

translate_base_url = 'http://translate.google.com/translate_tts'

captcha_base_url = 'http://ipv6.google.com/sorry/CaptchaRedirect'

continue_url = 'http://translate.google.com/translate_tts?ie=UTF-8&q=words&tl=en&q=what'

sound_path = 'static/sounds/%(lang)s/%(text)s.mp3'

s = requests.Session()

def create():
    lang = request.form['lang']
    text = request.form['text']

    # TODO: Bypass Google Translate if sound already exists in DB

    params = build_translate_url_params(lang, text)
    translate_url = translate_base_url + '?' + params

    r = s.get(translate_url)

    if r.status_code == 503:
        captcha = store_captcha(s, r.text)
        template = render_template('captcha.html', captcha=captcha, lang=lang,
                                   text=text)
        res = build_create_failure_response(template)
    elif r.status_code == 200:
        # TODO: Implement
        sound_path = save_sound(lang, text, r.content)
        res = { 'success': True }
        print 'It works!'
    else:
        # TODO: Implement
        pass

    return jsonify(**res)

def receive_captcha():
    idd = request.form['id']
    captcha = request.form['captcha']
    lang = request.form['lang']
    text = request.form['text']

    params = build_captcha_url_params(idd, captcha)
    captcha_url = captcha_base_url + '?' + params

    r = s.get(captcha_url)

    if r.status_code == 503:
        captcha = store_captcha(s, r.text)
        template = render_template('captcha.html', captcha=captcha, lang=lang,
                                   text=text)
        res = build_create_failure_response(template)
    elif r.status_code == 200:
        res = build_captcha_success_response(lang, text)
    else:
        # TODO return 500 or something
        pass

    return jsonify(**res)

def save_sound(lang, text, sound):
    pathText = "".join( map(to_file_path, text) )
    path = sound_path % { 'lang': lang, 'text': pathText }

    create_dir_if_not_exists('static/sounds/' + lang)

    f = open(path, 'w')
    f.write(sound)
    f.close()

    return path

def create_dir_if_not_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def to_file_path(c):
    switcher = {
        ' ': '_',
        '/': '-',
    }

    return switcher.get(c, c)

def build_create_failure_response(template):
    return {
        'success': False,
        'template': template
    }

def build_captcha_success_response(lang, text):
    return {
        'success': True,
        'lang': lang,
        'text': text
    }

def build_translate_url_params(lang, text):
    return urlencode({
        'ie': 'UTF-8',
        'tl': lang,
        'q' : text
    })

def build_captcha_url_params(idd, captcha):
    return urlencode({
        'continue': continue_url,
        'id': idd,
        'captcha': captcha,
        'submit': 'Submit'
    })
