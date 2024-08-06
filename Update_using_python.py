import mysql.connector
import schedule
import time
import random
import string
from datetime import datetime

db_config = {
  'host':"localhost",
  'user':"root",
  'password':"Kipithon@123",
  'database':"world"

 } 

tables = {}


def get_random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def get_random_int(min_value=1, max_value=100):
    return random.randint(min_value, max_value)

def make_random_changes(cursor):
    query_all = f"SELECT distinct referenced_table_name FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE where table_schema='world' and referenced_table_name is not null"
    cursor.execute(query_all)
    result = cursor.fetchall()
    
    for table, columns in tables.items():
            column = random.choice(columns)
            new_value = (get_random_string() if 'char' in column else
                        get_random_int() if 'int' in column else
                        datetime.now() if 'timestamp' in column else
                        None)
            query = f"UPDATE {table} SET {column} = %s ORDER BY RAND() LIMIT 1"
            for counter in range(random.randint(10,50)):
                cursor.execute(query, (new_value,))

def constraints(cursor):
    for table, columns in tables.items():
        query_all = f"SELECT table_name,column_name FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE where table_schema='world' and table_name='{table}' and (constraint_name='PRIMARY' or referenced_column_name is not NULL)"
        cursor.execute(query_all)
        result = cursor.fetchall()
        primary_foreign_dict = {}

        for key, value in result:
            if key not in primary_foreign_dict:
                primary_foreign_dict[key] = []
            primary_foreign_dict[key].append(value)

        for key in primary_foreign_dict:
            if key in tables:
                tables[key] = [item for item in tables[key] if item not in primary_foreign_dict[key]]

def main():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        tbl_lst = ['city','country','countrylanguage']

        for tbl in tbl_lst:
            query = f"SHOW COLUMNS FROM {tbl}"
            cursor.execute(query)
            columns = cursor.fetchall()
            column_names = [column[0] for column in columns]
            tables[tbl]=column_names
        constraints(cursor)
        print(tables)
        make_random_changes(cursor)

        conn.commit()
        print("Random changes committed successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
if __name__ == "__main__":
    main()
schedule.every(2).minutes.do(main)

while True:
  schedule.run_pending()
  time.sleep(1)



