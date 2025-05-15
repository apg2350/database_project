import sqlite3
import csv

conn = sqlite3.connect('robot.db')
cursor = conn.cursor()

# Drop tables if they already exist to avoid duplicates
cursor.execute('DROP TABLE IF EXISTS Robot;')
cursor.execute('DROP TABLE IF EXISTS SensorReading;')
cursor.execute('DROP TABLE IF EXISTS TargetInterval;')

# Create Robot table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Robot (
    RobotID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL
);''')

# Load robots from CSV
with open('robot.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        cursor.execute('INSERT OR IGNORE INTO Robot (RobotID, Name) VALUES (?, ?);', (int(row[0]), row[1]))

# Create SensorReading table
cursor.execute('''
CREATE TABLE IF NOT EXISTS SensorReading (
    ReadingID INTEGER PRIMARY KEY AUTOINCREMENT,
    RobotID INTEGER,
    X_Axis REAL,
    Y_Axis REAL,
    Timestamp INTEGER,
    FOREIGN KEY (RobotID) REFERENCES Robot(RobotID)
);''')

# Load sensor readings from t1.csv to t5.csv
for i in range(1, 6):
    filename = f't{i}.csv'
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        timestamp = 1
        for row in reader:
            try:
                x_axis, y_axis = map(float, row)
                cursor.execute('INSERT INTO SensorReading (RobotID, X_Axis, Y_Axis, Timestamp) VALUES (?, ?, ?, ?);', (i, x_axis, y_axis, timestamp))
                timestamp += 1
            except ValueError:
                print(f'Skipping invalid data: {row}')

# Create TargetInterval table
cursor.execute('''
CREATE TABLE IF NOT EXISTS TargetInterval (
    IntervalID INTEGER PRIMARY KEY AUTOINCREMENT,
    StartTime INTEGER,
    EndTime INTEGER,
    EventType TEXT
);''')

# Load target intervals from CSV
with open('target_interval.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        start_time, end_time, event_type = row
        cursor.execute('INSERT INTO TargetInterval (StartTime, EndTime, EventType) VALUES (?, ?, ?);', (int(start_time), int(end_time), event_type))

# Task 3: Max/Min X and Y axis per Robot
cursor.execute('''SELECT Name, MAX(X_Axis), MIN(X_Axis), MAX(Y_Axis), MIN(Y_Axis)
                 FROM Robot JOIN SensorReading ON Robot.RobotID = SensorReading.RobotID
                 GROUP BY Name;''')
print('Task 3: Max/Min X and Y axis per Robot:')
for row in cursor.fetchall():
    print(row)

# Task 4: Regions where 'Astro' and 'IamHuman' are close
cursor.execute('''SELECT s1.Timestamp, s1.X_Axis, s1.Y_Axis, s2.X_Axis, s2.Y_Axis
                 FROM SensorReading s1, SensorReading s2
                 WHERE s1.RobotID = 1 AND s2.RobotID = 2
                 AND ABS(s1.X_Axis - s2.X_Axis) < 1
                 AND ABS(s1.Y_Axis - s2.Y_Axis) < 1;''')
print('Task 4: Close regions between Astro and IamHuman:')
for row in cursor.fetchall():
    print(row)



# Commit and close connection
conn.commit()
conn.close()

print('Database setup and analysis complete.')
