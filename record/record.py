from typing import List
import sqlite3
import os
import sys
from parser.parser import *

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

def connect_to_database() -> sqlite3.Connection:
    if not os.path.exists(DATABASE_FILE):
        return create_database()
    return sqlite3.connect(DATABASE_FILE)

def add_entries(db_cursor: sqlite3.Cursor, listings: List[Listing]):
    for listing in listings:
        db_cursor.execute("INSERT INTO seen VALUES (?)", (int(listing.guid),))
