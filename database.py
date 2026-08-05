import sqlite3
import os


# ==========================================
# DATABASE PATH
# ==========================================

DB_PATH = "data/registrations.db"


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():

    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        registration_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        field TEXT NOT NULL,
        experience TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


# ==========================================
# SAVE REGISTRATION
# ==========================================

def save_to_database(registration):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO registrations
    (registration_id, name, email, field, experience)
    VALUES (?, ?, ?, ?, ?)
    """, (
        registration["registration_id"],
        registration["name"],
        registration["email"],
        registration["field"],
        registration["experience"]
    ))

    conn.commit()
    conn.close()


# ==========================================
# FIND REGISTRATION
# ==========================================

def find_registration(registration_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT registration_id, name, email, field, experience
    FROM registrations
    WHERE registration_id = ?
    """, (registration_id,))

    result = cursor.fetchone()

    conn.close()

    if result:

        return {
            "registration_id": result[0],
            "name": result[1],
            "email": result[2],
            "field": result[3],
            "experience": result[4]
        }

    return None