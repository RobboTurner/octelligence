import sqlite3
import csv

def load_db():
    # Connect to SQLite Database
    conn = sqlite3.connect('polling/data/polling.db')
    cursor = conn.cursor()

    # Create table with correct SQL syntax
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS polling (
        id INTEGER PRIMARY KEY,
        question TEXT NOT NULL,
        demographic TEXT NOT NULL,
        value FLOAT
    )
    ''')

    # Load data from a CSV file
    with open('polling/data/polling.csv', 'r') as file:
        # Assuming the CSV has no header row, else use next(reader) to skip it
        reader = csv.reader(file)
        for row in reader:
            cursor.execute('''
            INSERT INTO polling (question, demographic, value) VALUES (?, ?, ?)
            ''', row)

    # Commit changes
    conn.commit()

    # Query the database to verify the insertions
    cursor.execute('SELECT * FROM polling')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

# You can call the function to test it
load_db()
