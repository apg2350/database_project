import sqlite3

def task3(cursor):
    print("Task 3: Max/Min X-axis per Robot:")
    cursor.execute('''
        SELECT R.Name, MAX(S.X_Axis), MIN(S.X_Axis)
        FROM Robot R
        JOIN SensorReading S ON R.RobotID = S.RobotID
        GROUP BY R.Name;
    ''')
    for row in cursor.fetchall():
        print(row)

    print("\nTask 3: Max/Min Y-axis per Robot:")
    cursor.execute('''
        SELECT R.Name, MAX(S.Y_Axis), MIN(S.Y_Axis)
        FROM Robot R
        JOIN SensorReading S ON R.RobotID = S.RobotID
        GROUP BY R.Name;
    ''')
    for row in cursor.fetchall():
        print(row)

def task4(cursor, threshold=1):
    print("\nTask 4: Regions where 'Astro' and 'IamHuman' are close at each timestamp (threshold = 1 cm):")
    cursor.execute('''
        SELECT
          a.Timestamp,
          MIN(a.X_Axis) AS x_min,
          MAX(a.X_Axis) AS x_max,
          MIN(a.Y_Axis) AS y_min,
          MAX(a.Y_Axis) AS y_max
        FROM SensorReading a
        JOIN SensorReading b ON a.Timestamp = b.Timestamp
        JOIN Robot ra ON a.RobotID = ra.RobotID
        JOIN Robot rb ON b.RobotID = rb.RobotID
        WHERE ra.Name = 'Astro' AND rb.Name = 'IamHuman'
          AND ABS(a.X_Axis - b.X_Axis) < ?
          AND ABS(a.Y_Axis - b.Y_Axis) < ?
        GROUP BY a.Timestamp
        ORDER BY a.Timestamp;
    ''', (threshold, threshold))

    regions = cursor.fetchall()
    if regions:
        for r in regions:
            print(f"Timestamp: {r[0]}, X: [{r[1]}, {r[2]}], Y: [{r[3]}, {r[4]}]")
    else:
        print("No close regions found.")

    print("\nTask 4: Total seconds 'Astro' and 'IamHuman' are close (threshold = 1 cm):")
    cursor.execute('''
        SELECT COUNT(*)
        FROM SensorReading a
        JOIN SensorReading b ON a.Timestamp = b.Timestamp
        JOIN Robot ra ON a.RobotID = ra.RobotID
        JOIN Robot rb ON b.RobotID = rb.RobotID
        WHERE ra.Name = 'Astro' AND rb.Name = 'IamHuman'
          AND ABS(a.X_Axis - b.X_Axis) < ?
          AND ABS(a.Y_Axis - b.Y_Axis) < ?;
    ''', (threshold, threshold))

    count = cursor.fetchone()[0]
    print(count)

def main():
    conn = sqlite3.connect('robot.db')
    cursor = conn.cursor()

    task3(cursor)
    task4(cursor, threshold=1)

    conn.close()

if __name__ == "__main__":
    main()
