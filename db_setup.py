import sqlite3

# Path to your database file
DB_PATH = "data/companies.db"

# Connect and create tables
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Table to store company URLs
cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    url TEXT UNIQUE
)
""")

# Table to store seen job entries
cursor.execute("""
CREATE TABLE IF NOT EXISTS seen_jobs (
    job_id TEXT PRIMARY KEY
)
""")

conn.commit()
conn.close()
print("✅ Database initialized successfully.")
