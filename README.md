# database_project

CSCI4333 Database Project
Swarm Robot Trajectory Database
Swarm robots are tiny robots that can perform programmed actions independently without human interference. These tiny robots are crucial for many
real-world tasks (e.g. resource foraging). Yet, ensuring robot swarm system is
working properly can be challenging. Robots may damage and gradually lose
control for various reasons such as mechanism failures.
In this database project, you aim to design a data analysis system to help
detect potential weird issues existed in the system. In the first step, you design
database is similar to the simulation of the interaction presented in the real
world. Here are some basic data files:
1. robot.csv: Each robot has an id and name.
2. t1.csv to t5.csv For each robot, a sensor reading will record robot location
(x-axis, y-axis, measured by cm) at each time stamp (measured by second).
Each row in the file indicates a specific time stamp starting from 1.
3. target interval.csv: Each row in this file represents a time interval (defined by start time and end time) highlighted the target time interval.
Each interval is described by start time, end time, event type.
You need to design the database to help the researchers to check robot status.
Task 1: (5 pt) Write a ER Diagram and the relational schema to design
database. Note that the original storage format is not optimal for the database.
You need to redesign tables based on the ER Diagram that you think is the best
fit for the data.
Task 2: (5 pt) Build a database (named as robot.db) via Python and SQLite
and import the data in the CSV file into the database.

Task 3: (5 pt) Using SQL, return the following information related to meta-info
of the data (print out the query result is sufficient).
1. A table consists of the names of robots and the maximal x-axis, minimum
x-axis reached by this robot.
2. A table consists of the names of robots and the maximal y-axis, minimum
y-axis reached by this robot.

Task 4: (5 pt) Using SQL, write code to analyze the following info related to
robot trajectory:
1. Suppose we define two robots are close with each other if ‘both x-axis and
y-axis’ difference is smaller than 1 cm. Return all the regions (measured
by x min, x max, y min, y max) that robot “Astro” and “IamHuman”
are closed with each other.
2. For the same robots, measured how many secs that they are close with
each other.
3. (bonus) For all the target interval, calculate if the average robot moving
speed is smaller than 0.2 cm/s. You code should print out a table that
each row consists the interval id, and the answer (Yes or No). Feel free to
use python to print out this table.

The robot.py file creates the database and imports all of the files used for this project(t1, t2, t3, t4, t5, target_interval.csv, robot.csv)
The test.py file contains all of the SQL queries for tasks 3 and 4 as well as the bonus.

To create the database and import all the files, use the following command: python3 robot.py\
To run sql queries, use the following command: python3 test.py\
I tested the files using GitHub codespaces.
