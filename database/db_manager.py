import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "progress.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create lesson_progress table
cursor.execute("""
CREATE TABLE IF NOT EXISTS lesson_progress (
    lesson_title TEXT PRIMARY KEY,
    completed INTEGER DEFAULT 0
)
""")

# Create quiz_scores table
cursor.execute("""
CREATE TABLE IF NOT EXISTS quiz_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER,
    date_taken TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

# Create code_challenges table
cursor.execute("""
CREATE TABLE IF NOT EXISTS code_challenges (
    challenge_id TEXT PRIMARY KEY,
    completed INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("Database tables created successfully.")
