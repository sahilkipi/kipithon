import mysql.connector
import schedule
import time
import random
import string

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
    
    
    for table, columns in tables.items():
        query = f"DELETE FROM {table} ORDER BY RAND() LIMIT 1"
        for counter in range(random.randint(10,50)):
            cursor.execute(query)

def main():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        tbl_lst = ["city","country", "countrylanguage"]
        query_all = f"SELECT distinct referenced_table_name FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE where table_schema='world' and referenced_table_name is not null"
        cursor.execute(query_all)
        result = cursor.fetchall()
        result_list=[item[0] for item in result]
        filtered_lst=[item for item in tbl_lst if item not in result_list]
        print(filtered_lst)
        for tbl in filtered_lst:
            query = f"SHOW COLUMNS FROM {tbl}"
            cursor.execute(query)
            columns = cursor.fetchall()
            column_names = [column[0] for column in columns]
            tables[tbl]=column_names
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



