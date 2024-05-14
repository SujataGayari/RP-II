import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('parking.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table to store parking spot availability
cursor.execute('''CREATE TABLE IF NOT EXISTS parking_spots (
                    id INTEGER PRIMARY KEY,
                    location TEXT,
                    spot_number INTEGER,
                    available BOOLEAN
                )''')

# Add 20 parking spots for each location initially, all available
for location in ['A', 'B', 'C']:
    for spot_number in range(1, 21):
        cursor.execute('''INSERT INTO parking_spots (location, spot_number, available) VALUES (?, ?, ?)''', (location, spot_number, True))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database setup completed successfully.")
