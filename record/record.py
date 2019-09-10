import sqlite3
import os

DATABASE_FILE = "database.db"

def create_database() -> sqlite3.Connection:
    # Create an empty file
    try:
        open(DATABASE_FILE, 'a').close()
    except:
        sys.exit("Failed to create a database!")

    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute("CREATE TABLE seen (id int)")
    conn.commit()
    return conn

def connect() -> sqlite3.Connection:
    if not os.path.exists(DATABASE_FILE):
        return create_database()
    return sqlite3.connect(DATABASE_FILE)
