import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('SELECT Title, Author FROM Books WHERE ID = "2"')
rows = cur.fetchall()

for Title, Author in rows:
    print(f'Title: {Title}, Author: {Author}')

conn.close()

# Fetches Title and Author of Book at Row/ID 2

--------------------

import sqlite3
import pandas as pd

conn = sqlite3.connect("database.db")

tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'", conn)

for table in tables["name"]:
    print(f"\n=== {table} ===")
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    print(df.to_string(index=False))

conn.close()

# Fetches Entire db

----------------------------

import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

genre_updates = [
    ("science fiction", 1),
    ("Chivalric Satire", 2),
    ("Ergodic / Horror Fiction", 3),
    ("Epic Poetry", 4),
]

cur.executemany("UPDATE Books SET Genre = ? WHERE Id = ?", genre_updates)

conn.commit()
conn.close()

# Add genres to the table
----------------------------------

import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("UPDATE Books SET Read_Status = 'Reading' WHERE Title = 'Don Quixote'")

conn.commit()
conn.close()

# Update Read_status
