import sqlite3
<<<<<<< HEAD

DATABASE_NAME = "database/batch_planner.db"


def get_connection():
    """
    Creates and returns a SQLite database connection.
    """

    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection

=======
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
>>>>>>> e8568112bbd6275753fba240fe45b17c67c21592
