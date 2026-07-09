import sqlite3

DATABASE_NAME = "database/batch_planner.db"


def get_connection():
    """
    Creates and returns a SQLite database connection.
    """

    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection

