import sqlite3
import pandas as pd
import os

# Remove existing database file if it exists
if os.path.exists('robot.db'):
    os.remove('robot.db')
    print("Existing database deleted.")

# Create the database
conn = sqlite3.connect('robot.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Robot (
    RobotID INTEGER PRIMARY KEY,
    Name TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS SensorReading (
    ReadingID INTEGER PRIMARY KEY AUTOINCREMENT,
    RobotID INTEGER,
    Timestamp INTEGER,
    X_Axis REAL,
    Y_Axis REAL,
    FOREIGN KEY (RobotID) REFERENCES Robot(RobotID)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS TargetInterval (
    IntervalID INTEGER PRIMARY KEY AUTOINCREMENT,
    StartTime INTEGER,
    EndTime INTEGER,
    EventType TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS RobotInterval (
    RobotID INTEGER,
    IntervalID INTEGER,
    PRIMARY KEY (RobotID, IntervalID),
    FOREIGN KEY (RobotID) REFERENCES Robot(RobotID),
    FOREIGN KEY (IntervalID) REFERENCES TargetInterval(IntervalID)
);
''')

# Load and insert robot data
robots = pd.read_csv('robot.csv')
robots.columns = ['RobotID', 'Name']
robots.to_sql('Robot', conn, if_exists='replace', index=False)

# Load and insert sensor readings
tables = ['t1.csv', 't2.csv', 't3.csv', 't4.csv', 't5.csv']
for table in tables:
    robot_id = int(table[1])  # Extract robot ID from filename like 't1.csv'
    readings = pd.read_csv(table, header=None)
    readings.columns = ['X_Axis', 'Y_Axis']
    readings.insert(0, 'Timestamp', range(1, len(readings) + 1))
    readings.insert(0, 'RobotID', robot_id)
    readings.to_sql('SensorReading', conn, if_exists='append', index=False)

# Load and insert target intervals
target_intervals = pd.read_csv('target_interval.csv')
target_intervals.columns = ['StartTime', 'EndTime', 'EventType']
target_intervals.to_sql('TargetInterval', conn, if_exists='replace', index=False)

print("Database setup and data import complete.")

conn.commit()
conn.close()
