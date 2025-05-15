import sqlite3
import csv
import math

# Create and connect to the database
conn = sqlite3.connect('robot.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS Robot (
    RobotID INTEGER PRIMARY KEY,
    Name TEXT
);''')
cursor.execute('''CREATE TABLE IF NOT EXISTS SensorReading (
    RobotID INTEGER,
    X_Axis REAL,
    Y_Axis REAL,
    Timestamp INTEGER,
    FOREIGN KEY(RobotID) REFERENCES Robot(RobotID)
);''')
cursor.execute('''CREATE TABLE IF NOT EXISTS TargetInterval (
    StartTime INTEGER,
    EndTime INTEGER,
    EventType TEXT
);''')

# Import robots
with open('robot.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        cursor.execute('INSERT INTO Robot (RobotID, Name) VALUES (?, ?);', (int(row[0]), row[1]))

# Import sensor readings
for i in range(1, 6):
    with open(f't{i}.csv', 'r') as file:
        reader = csv.reader(file)
        timestamp = 1
        for row in reader:
            try:
                x_axis = float(row[0])
                y_axis = float(row[1])
                cursor.execute('INSERT INTO SensorReading (RobotID, X_Axis, Y_Axis, Timestamp) VALUES (?, ?, ?, ?);', (i, x_axis, y_axis, timestamp))
                timestamp += 1
            except ValueError:
                continue

# Import target intervals
with open('target_interval.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        cursor.execute('INSERT INTO TargetInterval (StartTime, EndTime, EventType) VALUES (?, ?, ?);', (int(row[0]), int(row[1]), row[2]))

# Commit the changes
conn.commit()

# Bonus Task: Calculate average speed per interval
print('\nBonus Task: Average speed check (threshold = 0.2 cm/s)')
query_speed = '''
SELECT ti.rowid, 
       AVG((SQRT((sr2.X_Axis - sr1.X_Axis) * (sr2.X_Axis - sr1.X_Axis) + 
                (sr2.Y_Axis - sr1.Y_Axis) * (sr2.Y_Axis - sr1.Y_Axis))) / (sr2.Timestamp - sr1.Timestamp)) AS avg_speed
FROM SensorReading sr1
JOIN SensorReading sr2 ON sr1.RobotID = sr2.RobotID AND sr2.Timestamp = sr1.Timestamp + 1
JOIN TargetInterval ti ON sr1.Timestamp BETWEEN ti.StartTime AND ti.EndTime
GROUP BY ti.rowid;
'''
cursor.execute(query_speed)
for row in cursor.fetchall():
    interval_id, avg_speed = row
    result = 'Yes' if avg_speed < 0.2 else 'No'
    print(f'Interval {interval_id}: {result}')

# Close the connection
conn.close()
