# Delete all files from Sound of Text older than one month.

import sqlite3, datetime, os

today = datetime.date.today()
ONE_MONTH_AGO = today - datetime.timedelta(days=30)

conn = sqlite3.connect('sounds.db')
c = conn.cursor()
c.row_factory = sqlite3.Row

res = c.execute('SELECT * FROM SOUNDS ORDER BY accessed ASC')

for row in res.fetchall():
    access_date = datetime.datetime.utcfromtimestamp(row['accessed']).date()
    if access_date < ONE_MONTH_AGO:
        c.execute('DELETE FROM SOUNDS WHERE id=?', [row['id']])
        try:
            os.remove(row['path'])
        except OSError as e:
            print e


conn.commit()
c.close()
