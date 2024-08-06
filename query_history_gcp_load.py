import os
from google.cloud import storage
import mysql.connector
import csv
import datetime

# Set the environment variable for authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/ShauryaNigam/Downloads/spiritual-craft-430907-a0-29f36d97a2c5.json"

# Get the current date
now = datetime.datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kipithon@123",
        database="world"
    )
    mycursor = mydb.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit()

query = """
SELECT query, db AS db_name, full_scan, exec_count, avg_latency, rows_sent, rows_affected, first_seen, last_seen
FROM sys.x$statement_analysis
WHERE db IS NOT NULL AND db NOT IN ('information_schema', 'sys')
AND (query LIKE 'SELECT%' OR query LIKE 'INSERT%' OR query LIKE 'UPDATE%' OR query LIKE 'DELETE%')
ORDER BY last_seen DESC;
"""

try:
    mycursor.execute(query)
    results = mycursor.fetchall()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    mycursor.close()
    mydb.close()
    exit()

# Get column names
column_names = [i[0] for i in mycursor.description]

# Define the local CSV file path
local_csv_file_path = f"C:/Users/ShauryaNigam/Desktop/query_history_backup/{year}_{month}_{day}_query_hist.csv"

# Output results to a local CSV file
try:
    with open(local_csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)
        writer.writerows(results)
except IOError as e:
    print(f"Error writing to CSV file: {e}")

# Upload the CSV file to Google Cloud Storage
def upload_to_gcs(local_file_path, bucket_name, gcs_file_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_file_path)
    blob.upload_from_filename(local_file_path)
    print(f"File {local_file_path} uploaded to {gcs_file_path} in bucket {bucket_name}.")

bucket_name = "mysql_db_migration" 
gcs_file_path = f"query_history_backup/{year}_{month}_{day}_query_hist.csv"

try:
    upload_to_gcs(local_csv_file_path, bucket_name, gcs_file_path)
except Exception as e:
    print(f"Error uploading to GCS: {e}")

mycursor.close()
mydb.close()

# Delete the local file after uploading
try:
    os.remove(local_csv_file_path)
except Exception as e:
    print(f"Error deleting the local file: {e}")
