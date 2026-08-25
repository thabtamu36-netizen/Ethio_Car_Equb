import sqlite3

DB = 'ethio_car_equb.db'

con = sqlite3.connect(DB)
cur = con.cursor()
cur.execute("SELECT id, participant_number, participant_name, status, verified_at FROM payments WHERE status='APPROVED' ORDER BY verified_at DESC LIMIT 5;")
rows = cur.fetchall()
print('Latest approved payments (most recent first):')
for r in rows:
    print(r)
con.close()
