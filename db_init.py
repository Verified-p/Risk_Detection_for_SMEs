import sqlite3
import os

DB_PATH = os.path.join("data", "trustlens.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Create audit table with all needed columns if it doesn't exist
cur.execute("""
CREATE TABLE IF NOT EXISTS audit (
    event TEXT,
    risk REAL,
    blocked INTEGER DEFAULT 0,
    credentials_rotated INTEGER DEFAULT 0,
    verified INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print(f"Database initialized at {DB_PATH}")