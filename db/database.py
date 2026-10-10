import sqlite3
from pathlib import Path

# Current project root
BASE_DIR = Path(__file__).resolve().parent

# Database path
DATABASE_PATH = BASE_DIR / "hr.db"


def get_connection():
    """
    Returns SQLite Connection
    """

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    return connection