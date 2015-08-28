from flask import request, jsonify, render_template, abort
from urllib import urlencode, quote
from model import insert_sound, get_sound_by_id, sound_exists
from model import get_sound_by_lang_text_pair
from model import store_captcha, save_sound, sounds_dir, img_path
from helpers.languages import languages
import requests
import urlparse
import os
import time

translate_base_url = 'http://translate.google.com/translate_tts'

captcha_base_url = 'http://google.com/sorry/CaptchaRedirect'

continue_url = 'http://translate.google.com/translate_tts?ie=UTF-8&q=words&tl=en&q=what'

curr_captcha_id = None

s = requests.Session()
s.headers.update({ 'User-Agent': 'SoundOfTextBot (soundoftext.com)' })

def create():
    global curr_captcha_id

    lang = request.form['lang']
    text = request.form['text'].strip().lower()[:100]

    if sound_exists(lang, text):
        sound = get_sound_by_lang_text_pair(lang, text)
        res = { 'success': True, 'id': sound[0] }
    elif curr_captcha_id:
        img = img_path + '?nocache=' + str(time.time())
        template = render_template('captcha.html', img=img, lang=lang,
                                   text=text, idd=curr_captcha_id)
        res = build_create_failure_response(template)
    else:
        params = build_translate_url_params(lang, text)
        translate_url = translate_base_url + '?' + params

        r = s.get(translate_url)

        global captcha_base_url
        captcha_base_url = urlparse.urljoin(r.url, '/sorry/CaptchaRedirect')

        if r.status_code == 503:
            curr_captcha_id = store_captcha(s, r.text)
            img = img_path + '?nocache=' + str(time.time())
            template = render_template('captcha.html', img=img, lang=lang,
                                       text=text, idd=curr_captcha_id)
            res = build_create_failure_response(template)
        elif r.status_code == 200:
            sound_path = save_sound(lang, text, r.content)
            idd = insert_sound(lang, text, sound_path)
            res = { 'success': True, 'id': idd }
        else:
            abort(500)

    return jsonify(**res)

def get_sound(idd):
    sound = get_sound_by_id(idd)
    lang = languages[ sound[1] ]
    text = sound[2]

    filename = os.path.basename(sound[3])
    safe_filename = quote(filename.encode('utf-8'))
    path = os.path.join('/static/sounds', sound[1], safe_filename)

    return render_template('sound.html', lang=lang, text=text, path=path)

def receive_captcha():
    global curr_captcha_id

    idd = request.form['id']
    captcha = request.form['captcha']
    lang = request.form['lang']
    text = request.form['text']

    # short circuit in case multiple users get a captcha at same time
    if not curr_captcha_id:
        return jsonify(**build_captcha_success_response(lang, text))

    params = build_captcha_url_params(idd, captcha)
    captcha_url = captcha_base_url + '?' + params

    r = s.get(captcha_url)

    if r.status_code == 503:
        captcha = store_captcha(s, r.text)
        template = render_template('captcha.html', captcha=captcha, lang=lang,
                                   text=text)
        res = build_create_failure_response(template)
    elif r.status_code == 200:
        curr_captcha_id = None

        res = build_captcha_success_response(lang, text)
    else:
        abort(500)

    return jsonify(**res)

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
        'q' : text.encode('utf-8')
    })

def build_captcha_url_params(idd, captcha):
    return urlencode({
        'continue': continue_url,
        'id': idd,
        'captcha': captcha,
        'submit': 'Submit'
    })
