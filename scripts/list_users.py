import sqlite3
import json

con = sqlite3.connect('ethio_car_equb.db')
cur = con.cursor()
cur.execute("SELECT id, participant_name, phone, telegram_username FROM users ORDER BY id;")
rows = cur.fetchall()
print(json.dumps([list(r) for r in rows], indent=2))
con.close()
