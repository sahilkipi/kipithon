import mysql.connector
import csv
import datetime

now = datetime.datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql123",
    database="demo_db"
)

mycursor = mydb.cursor()

# Query History - Query. Similarly for Inventory details query
query = "select query, db As db_name, full_scan, exec_count, avg_latency, rows_sent, rows_affected,first_seen, last_seen\
        from sys.x$statement_analysis\
        WHERE db IS NOT NULL AND db NOT IN ('information_schema', 'sys')\
        AND (query LIKE ('SELECT%') OR query LIKE ('INSERT%')\
        OR query LIKE ('INSERT%') OR query LIKE ('INSERT%') )\
        ORDER BY last_seen DESC;"


mycursor.execute(query)
results = mycursor.fetchall()

column_names = [i[0] for i in mycursor.description]

csv_file_path = f"C:/Users/WankvaniNitinTeekamd/Desktop/query_history_backup/{year}_{month}_{day}_query_hist.csv"

# Output results to CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(column_names)
    writer.writerows(results)

mycursor.close()
mydb.close()

