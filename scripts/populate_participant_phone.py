import sqlite3
import json

con = sqlite3.connect('ethio_car_equb.db')
cur = con.cursor()
cur.execute("UPDATE payments SET participant_phone = (SELECT phone FROM users WHERE users.id = payments.user_id) WHERE participant_phone IS NULL;")
con.commit()
cur.execute("SELECT id, participant_number, participant_name, participant_phone, status, verified_at FROM payments WHERE status='APPROVED' ORDER BY verified_at ASC;")
rows = cur.fetchall()
print(json.dumps([list(r) for r in rows], default=str, indent=2))
con.close()
