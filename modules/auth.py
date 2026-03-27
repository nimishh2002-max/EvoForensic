import sqlite3
import os

# =====================================================================
# CONFIGURATION & PATHS
# =====================================================================
# Automatically resolve path to MainProject/data/forensic.db
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DB_DIR, "forensic.db")

def init_db():
    """Initializes the users database table if it doesn't exist."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            full_name TEXT,
            badge_id TEXT,
            department TEXT,
            location TEXT,
            official_email TEXT,
            phone TEXT
        )
    """)
    conn.commit()
    conn.close()

def login_user(username, password):
    """Verifies user credentials."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if row and row[0] == password:
        return True
    return False

def register_user(username, password, full_name, badge_id, department, location, official_email, phone):
    """Registers a new investigator in the system."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO users 
            (username, password, full_name, badge_id, department, location, official_email, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, password, full_name, badge_id, department, location, official_email, phone))
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists."