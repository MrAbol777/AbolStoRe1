import sqlite3
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%accounts%'")
tables = [row[0] for row in cursor.fetchall()]
print("Accounts tables:", tables)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%orders%'")
tables = [row[0] for row in cursor.fetchall()]
print("Orders tables:", tables)
conn.close()