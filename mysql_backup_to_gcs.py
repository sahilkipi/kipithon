import os
from google.cloud import storage
import mysql.connector
import csv
import datetime
import json
from google.cloud import secretmanager

# Set the environment variable for authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/RushikeshDighe/Desktop/KIPITHON/GCP_SETUP/spiritual-craft-430907-a0-29f36d97a2c5.json"

# GCP project and secret details
project_id = "spiritual-craft-430907-a0"  # Replace with your GCP project ID
secret_id = "kipithon-key"  # Replace with your secret ID

# Function to access the secret from GCP Secret Manager
def access_secret_version(project_id, secret_id,version_id=1):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return payload

# Access the secret (JSON key)
json_key = access_secret_version(project_id, secret_id,1)
json_key_dict = json.loads(json_key)

# Authenticate with the JSON key
storage_client = storage.Client.from_service_account_info(json_key_dict)

# Get the current date
now = datetime.datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")

# Upload the CSV file to Google Cloud Storage
def upload_to_gcs(local_file_path, bucket_name, gcs_file_path):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_file_path)
    blob.upload_from_filename(local_file_path)
    print(f"File {local_file_path} uploaded to {gcs_file_path} in bucket {bucket_name}.")

def execute_query_and_upload(query, task_folder_name):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="Adventureworks2014"
        )
        mycursor = mydb.cursor()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return

    try:
        mycursor.execute(query)
        results = mycursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mycursor.close()
        mydb.close()
        return

    # Get column names
    column_names = [i[0] for i in mycursor.description]

    # Define the local CSV file path
    local_csv_file_path = f"C:/Users/RushikeshDighe/Desktop/KIPITHON/Backups And Overviews/{task_folder_name}/{year}_{month}_{day}.csv"

    # Output results to a local CSV file
    try:
        with open(local_csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)
            writer.writerows(results)
    except IOError as e:
        print(f"Error writing to CSV file: {e}")
        return

    bucket_name = "mysql_db_migration"
    gcs_file_path = f"{task_folder_name}/{year}_{month}_{day}.csv"

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

# Queries
object_overview_query = """
SELECT * FROM sys.schema_object_overview
where db not in ('sys','information_schema','performance_schema','mysql');
"""

query_history_query = """
SELECT query, db AS db_name, full_scan, exec_count, err_count, total_latency, max_latency, avg_latency, rows_sent, rows_examined, rows_affected, max_total_memory, 
first_seen, last_seen,current_timestamp() as ingest_tmst
FROM sys.x$statement_analysis
WHERE db IS NOT NULL AND db NOT IN ('information_schema', 'sys')
AND (query LIKE 'SELECT%' OR query LIKE 'INSERT%' OR query LIKE 'UPDATE%' OR query LIKE 'DELETE%')
ORDER BY last_seen DESC;
"""

schema_memory_datails = """ 
SELECT TABLE_SCHEMA, TABLE_NAME,TABLE_TYPE,
Data_length,index_length FROM information_schema.tables
WHERE TABLE_SCHEMA NOT IN ('information_schema', 'sys','performance_schema', 'mysql');
"""

schema_performance_stats = """
SELECT statements, statement_latency, table_scans, total_connections, current_memory, total_memory_allocated,
current_date() as ingest_date
FROM sys.host_summary;
"""

views_dependencies_info ="""
SELECT  views.TABLE_NAME As VIEW, tab.TABLE_SCHEMA as DB_NAME, tab.TABLE_NAME AS PARENT
FROM information_schema.TABLES AS tab 
INNER JOIN information_schema.VIEWS AS views 
ON views.VIEW_DEFINITION LIKE CONCAT('%`',tab.TABLE_NAME,'`%') and
tab.TABLE_SCHEMA = views.table_schema
WHERE tab.table_schema not in ('sys','information_schema','performance_schema','mysql')
and views.table_schema not in ('sys','information_schema','performance_schema','mysql') ;
"""


# Task folder names and queries
task_folders = [
    ("DB_OBJECT_OVERVIEW", object_overview_query),
    ("Query_History_Backup", query_history_query),
    ("Schema_memory_datails",schema_memory_datails),
    ("Schema_performance_stats", schema_performance_stats),
    ("Views_dependencies_info",views_dependencies_info)

]

# Execute queries and upload
for task_folder_name, query in task_folders:
    execute_query_and_upload(query, task_folder_name)