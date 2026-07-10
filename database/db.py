import sqlite3
import os

# Get the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database file path
DB_PATH = os.path.join(BASE_DIR, "batch_planner.db")

# Schema file path
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


def initialize_database():
    """Create database tables from schema.sql"""

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

    print("✅ Database initialized successfully.")


if __name__ == "__main__":
    initialize_database()