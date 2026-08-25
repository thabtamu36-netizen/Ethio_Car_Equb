import sqlite3
import json

# Mapping: participant_number, full name, phone
mapping = [
    (1, "Toni Boy", "0941234567"),
]

con = sqlite3.connect('ethio_car_equb.db')
cur = con.cursor()
results = []
for part_no, name, phone in mapping:
    cur.execute(
        "UPDATE payments SET participant_name = ?, participant_phone = ? WHERE participant_number = ? AND status = 'APPROVED'",
        (name, phone, part_no)
    )
    con.commit()
    cur.execute(
        "SELECT id, participant_number, participant_name, participant_phone, status, verified_at FROM payments WHERE participant_number = ? AND status = 'APPROVED' ORDER BY verified_at ASC",
        (part_no,)
    )
    rows = cur.fetchall()
    for r in rows:
        results.append({
            'id': r[0],
            'participant_number': r[1],
            'participant_name': r[2],
            'participant_phone': r[3],
            'status': r[4],
            'verified_at': str(r[5])
        })

print(json.dumps(results, indent=2))
con.close()
