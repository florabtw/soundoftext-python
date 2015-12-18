from flask import request, jsonify, render_template, abort
from urllib import urlencode, quote
from model import insert_sound, get_sound_by_id, sound_exists
from model import get_sound_by_lang_text_pair, save_sound, sounds_dir
from helpers.languages import languages
import requests
import os
import execjs

translate_base_url = 'http://translate.google.com/translate_tts'

s = requests.Session()
s.headers.update({ 'User-Agent': 'SoundOfTextBot (soundoftext.com)' })

current_dir = os.path.abspath(os.path.dirname(__file__))
HASHJS_PATH = os.path.join(current_dir, 'hash.js')

# javascript hash function
hashjs_file = open(HASHJS_PATH, 'r')
hashjs = execjs.compile( hashjs_file.read() )
hashjs_file.close()

def create():
    lang = request.form['lang']
    text = request.form['text'].strip().lower()[:100]

    if sound_exists(lang, text):
        sound = get_sound_by_lang_text_pair(lang, text)
        res = { 'success': True, 'id': sound[0] }
    else:
        params = build_translate_url_params(lang, text)
        translate_url = translate_base_url + '?' + params

        r = s.get(translate_url)

        if r.status_code == 200:
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

def build_translate_url_params(lang, text):
    hashed = hashjs.call('TL', text)

    return urlencode({
        'ie': 'UTF-8',
        'tl': lang,
        'q' : text.encode('utf-8'),
        'client': 't',
        'tk'    : hashed
    })
