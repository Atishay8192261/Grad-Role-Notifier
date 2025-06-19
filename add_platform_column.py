import sqlite3

conn = sqlite3.connect("data/companies.db")
c = conn.cursor()

# Add 'platform' column if it doesn't exist
try:
    c.execute("ALTER TABLE companies ADD COLUMN platform TEXT")
    print("✅ Column 'platform' added.")
except sqlite3.OperationalError:
    print("ℹ️ Column already exists. Skipping.")

conn.commit()
conn.close()
