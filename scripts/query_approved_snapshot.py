import sqlite3
import json

con = sqlite3.connect('ethio_car_equb.db')
cur = con.cursor()
# join users to get phone/telegram_username (payments stores participant_name snapshot)
cur.execute(
    """
    SELECT p.id, p.user_id, p.participant_number, p.participant_name,
           u.phone, u.telegram_username, p.status, p.verified_at
    FROM payments p
    JOIN users u ON p.user_id = u.id
    WHERE p.status='APPROVED'
    ORDER BY p.verified_at ASC
    LIMIT 20
    """
)
rows = cur.fetchall()
output = []
for r in rows:
    output.append({
        'id': r[0],
        'user_id': r[1],
        'participant_number': r[2],
        'participant_name': r[3],
        'phone': r[4],
        'telegram_username': r[5],
        'status': r[6],
        'verified_at': str(r[7])
    })
print(json.dumps(output, indent=2))
con.close()
