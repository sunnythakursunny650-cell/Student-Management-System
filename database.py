import sqlite3
from pathlib import Path

# =========================================================
# DATABASE PATH
# =========================================================

DB_PATH = Path(__file__).parent / "students.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# =========================================================
# CREATE STUDENTS TABLE
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    mobile TEXT,
    gender TEXT,
    date_of_birth TEXT,
    course TEXT NOT NULL,
    attendance REAL DEFAULT 0,
    marks REAL DEFAULT 0,
    grade TEXT,
    status TEXT
)
""")


# =========================================================
# SAVE CHANGES
# =========================================================

conn.commit()
conn.close()

print("Student Database Created Successfully ✅")