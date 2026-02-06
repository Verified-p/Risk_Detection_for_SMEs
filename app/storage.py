import sqlite3
from datetime import datetime
from app.config import DB_PATH


def log(event: dict, risk: int, reasons: list):
    """
    Store security audit logs safely.
    No sensitive data should reach here (already sanitized).
    """

    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            event TEXT,
            risk INTEGER,
            reasons TEXT
        )
    """)

    # Insert audit record
    cursor.execute(
        "INSERT INTO audit (timestamp, event, risk, reasons) VALUES (?, ?, ?, ?)",
        (
            datetime.utcnow().isoformat(),
            str(event),
            risk,
            "; ".join(reasons)
        )
    )

    db.commit()
    db.close()
