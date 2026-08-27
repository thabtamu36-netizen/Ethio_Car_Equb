from database import get_db
from sqlalchemy import text

db = get_db()

try:
    result = db.execute(
        text("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE'
            ORDER BY table_schema, table_name
        """)
    )

    print("\nDATABASE TABLES:")

    rows = result.fetchall()

    if not rows:
        print("NO TABLES FOUND")

    for row in rows:
        print(row)

finally:
    db.close()