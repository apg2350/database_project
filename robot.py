import sqlite3
import csv
import os

# Files and robot ID mapping
robot_csv = 'robot.csv'
robot_files = {
    't1.csv': 1,  # Astro
    't2.csv': 2,  # IamHuman
    't3.csv': 3,  # MoonLander
    't4.csv': 4,  # Wonderlust
    't5.csv': 5,  # Challenger
}

# Connect to SQLite DB (creates if not exists)
conn = sqlite3.connect('robot.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Robot (
    RobotID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL UNIQUE
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS SensorReading (
    ReadingID INTEGER PRIMARY KEY AUTOINCREMENT,
    RobotID INTEGER,
    X_Axis REAL,
    Y_Axis REAL,
    Timestamp INTEGER,
    FOREIGN KEY (RobotID) REFERENCES Robot(RobotID)
);
''')

conn.commit()

# Import robots from robot.csv
print("Importing robots...")
with open(robot_csv, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) < 2:
            continue
        robot_id = int(row[0])
        robot_name = row[1].strip()
        cursor.execute('INSERT OR IGNORE INTO Robot (RobotID, Name) VALUES (?, ?)', (robot_id, robot_name))
conn.commit()

# Import sensor readings for each robot file
print("Importing sensor readings...")
for filename, robot_id in robot_files.items():
    if not os.path.exists(filename):
        print(f"Warning: File {filename} not found. Skipping.")
        continue

    with open(filename, newline='') as f:
        reader = csv.reader(f)
        timestamp = 1
        for row in reader:
            if len(row) < 2:
                timestamp += 1
                continue
            x_str, y_str = row[0].strip(), row[1].strip()
            # Skip rows with unknown or invalid data
            try:
                x = float(x_str)
                y = float(y_str)
            except ValueError:
                timestamp += 1
                continue
            
            cursor.execute('''
                INSERT INTO SensorReading (RobotID, X_Axis, Y_Axis, Timestamp)
                VALUES (?, ?, ?, ?)
            ''', (robot_id, x, y, timestamp))
            timestamp += 1

conn.commit()
conn.close()
print("Data import complete.")
