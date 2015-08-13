from flask import g
import sqlite3

insert_query = 'INSERT INTO sounds (lang, text, path) values (?, ?, ?)'

select_path_query = 'SELECT * FROM sounds WHERE path = ?'

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
