from flask import g
import sqlite3
import os
import errno

insert_query = 'INSERT INTO sounds (lang, text, path) values (?, ?, ?)'

select_path_query = 'SELECT * FROM sounds WHERE path = ?'

select_idd_query = 'SELECT * FROM sounds WHERE id = ?'

select_lang_text_query = 'SELECT * FROM sounds WHERE lang = ? AND text = ?'

# returns id of new sound
def insert_sound(lang, text, path):
    cur = g.db.execute(insert_query, [lang, text, path])
    g.db.commit()

    sound = get_sound_by_path(path)
    return sound[0]

def get_sound_by_path(path):
    cur = g.db.execute(select_path_query, [path])
    return cur.fetchone()

def get_sound_by_id(idd):
    cur = g.db.execute(select_idd_query, [idd])
    return cur.fetchone()

def sound_exists(lang, text):
    cur = g.db.execute(select_lang_text_query, [lang, text])
    res = cur.fetchone()
    return res is not None

def get_sound_by_lang_text_pair(lang, text):
    cur = g.db.execute(select_lang_text_query, [lang, text])
    return cur.fetchone()

sound_path = 'static/sounds/%(lang)s/%(text)s.mp3'

# get absolute path to sounds directory
current_dir = os.path.dirname(__file__)
sounds_dir = os.path.join(current_dir, '../static/sounds')
sounds_dir = os.path.abspath(sounds_dir)

def save_sound(lang, text, sound):
    pathText = "".join( map(to_file_path, text) )
    lang_dir = os.path.join(sounds_dir, lang)
    sound_path = os.path.join(lang_dir, '%s.mp3' % pathText)

    create_dir_if_not_exists(os.path.dirname(sound_path))

    f = open(sound_path, 'w')
    f.write(sound)
    f.close()

    return sound_path

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
