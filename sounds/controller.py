from flask import request, jsonify

translate_base_url = 'http://translate.google.com/translate_tts'

def create():
    lang = request.form['lang']
    text = request.form['text']

    res = build_create_response(False)
    return jsonify(**res)

def build_create_response(success):
    return {
        'success': success
    }

def build_translate_url_params(lang, text):
    return {
        'ie': 'UTF-8',
        'tl': lang,
        'q' : text
    }
