import sqlite3

conn = sqlite3.connect('eisapp.db')
c = conn.cursor()

c.execute('CREATE TABLE users (username text, nfcid text, amount real)')
c.execute("INSERT INTO users VALUES ('test','a1b2',100)")
conn.commit()
conn.close()
