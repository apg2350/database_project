import sqlite3

conn = sqlite3.connect('robot.db')
cursor = conn.cursor()

# --- Task 3 ---

print("Task 3: Max/Min X-axis per Robot:")
query_task3_x = '''
SELECT R.Name, MAX(S.X_Axis) AS Max_X, MIN(S.X_Axis) AS Min_X
FROM Robot R
JOIN SensorReading S ON R.RobotID = S.RobotID
GROUP BY R.Name;
'''
cursor.execute(query_task3_x)
for row in cursor.fetchall():
    print(row)

print("\nTask 3: Max/Min Y-axis per Robot:")
query_task3_y = '''
SELECT R.Name, MAX(S.Y_Axis) AS Max_Y, MIN(S.Y_Axis) AS Min_Y
FROM Robot R
JOIN SensorReading S ON R.RobotID = S.RobotID
GROUP BY R.Name;
'''
cursor.execute(query_task3_y)
for row in cursor.fetchall():
    print(row)

# --- Task 4 (Updated for Astro and IamHuman with threshold 1 cm) ---

print("\nTask 4: Regions where 'Astro' and 'IamHuman' are close at each timestamp (threshold = 1 cm):")
query_task4_regions = '''
SELECT
  MIN(a.X_Axis) AS x_min,
  MAX(a.X_Axis) AS x_max,
  MIN(a.Y_Axis) AS y_min,
  MAX(a.Y_Axis) AS y_max,
  a.Timestamp
FROM SensorReading a
JOIN SensorReading b ON a.Timestamp = b.Timestamp
JOIN Robot ra ON a.RobotID = ra.RobotID
JOIN Robot rb ON b.RobotID = rb.RobotID
WHERE ra.Name = 'Astro' AND rb.Name = 'IamHuman'
  AND ABS(a.X_Axis - b.X_Axis) < 1
  AND ABS(a.Y_Axis - b.Y_Axis) < 1
GROUP BY a.Timestamp
ORDER BY a.Timestamp;
'''
cursor.execute(query_task4_regions)
regions = cursor.fetchall()
if regions:
    for row in regions:
        print(row)
else:
    print("No close regions found.")

print("\nTask 4: Total seconds 'Astro' and 'IamHuman' are close (threshold = 1 cm):")
query_task4_count = '''
SELECT COUNT(*) 
FROM SensorReading a
JOIN SensorReading b ON a.Timestamp = b.Timestamp
JOIN Robot ra ON a.RobotID = ra.RobotID
JOIN Robot rb ON b.RobotID = rb.RobotID
WHERE ra.Name = 'Astro' AND rb.Name = 'IamHuman'
  AND ABS(a.X_Axis - b.X_Axis) < 1
  AND ABS(a.Y_Axis - b.Y_Axis) < 1;
'''
cursor.execute(query_task4_count)
count = cursor.fetchone()[0]
print(count)

conn.close()
