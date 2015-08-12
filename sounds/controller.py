from flask import request, jsonify, render_template
from urllib import urlencode
from captcha import store_captcha
import requests

translate_base_url = 'http://translate.google.com/translate_tts'

s = requests.Session()

def create():
    lang = request.form['lang']
    text = request.form['text']

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
        res = { 'success': True }
        print 'It works!'
    else:
        # TODO: Implement
        pass

    return jsonify(**res)

def build_create_failure_response(template):
    return {
        'success': False,
        'template': template
    }

def build_translate_url_params(lang, text):
    return urlencode({
        'ie': 'UTF-8',
        'tl': lang,
        'q' : text
    })
