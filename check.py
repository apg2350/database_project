import sqlite3

def task4_close_seconds(db_path='robot.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = '''
    SELECT COUNT(*) FROM (
        SELECT s1.Timestamp
        FROM SensorReading s1
        JOIN SensorReading s2 ON s1.Timestamp = s2.Timestamp
        WHERE s1.RobotID = 1  -- Astro
          AND s2.RobotID = 2  -- IamHuman
          AND ABS(s1.X_Axis - s2.X_Axis) < 1
          AND ABS(s1.Y_Axis - s2.Y_Axis) < 1
    );
    '''

    cursor.execute(query)
    close_seconds = cursor.fetchone()[0]

    print(f"Task 4: Total seconds 'Astro' and 'IamHuman' are close: {close_seconds}")

    conn.close()

if __name__ == "__main__":
    task4_close_seconds()
