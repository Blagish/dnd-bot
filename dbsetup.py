import sqlite3

conn = sqlite3.connect("data.db")
cur = conn.cursor();

cur.execute('''CREATE TABLE rollstats
        (id text, rollcount int, rollavg double)''')

conn.commit()
conn.close()

