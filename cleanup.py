# Delete all files from Sound of Text older than one month.

import sqlite3, datetime, os

today = datetime.date.today()
ONE_MONTH_AGO = today - datetime.timedelta(days=30)

def deleteRow(row):
    delete.execute('DELETE FROM SOUNDS WHERE id=?', [row['id']])
    try:
        os.remove(row['path'])
    except OSError as e:
        print e

conn = sqlite3.connect('sounds.db')
conn.row_factory = sqlite3.Row

select = conn.cursor()
delete = conn.cursor()

select.execute('SELECT * FROM SOUNDS ORDER BY accessed ASC')

rows = select.fetchmany(100)
while (len(rows) != 0):
    for row in rows:
        if row['accessed'] == None:
            print row
            deleteRow(row)
            continue

        access_date = datetime.datetime.utcfromtimestamp(row['accessed']).date()
        if access_date < ONE_MONTH_AGO:
            deleteRow(row)
    rows = select.fetchmany(100)

conn.commit()
select.close()
delete.close()
