import mysql.connector
import schedule
import time
import random



mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql123",
  database="demo_db"
)

mycursor = mydb.cursor()

def execute_queries():
    tbl_lst = ["homes", "mlb_teams_2012", "mlb_players"]
    tables = {}
    for tbl in tbl_lst:
        query = f"SHOW COLUMNS FROM {tbl}"
        mycursor.execute(query)
        columns = mycursor.fetchall()
        column_names = [column[0] for column in columns]
        tables[tbl]=column_names
    print(tables)

    # Working for Select
    for i in range(200):
        print(f"Iteration: {i + 1}")
        for table, columns in tables.items():
            query_all = f"SELECT * FROM {table}"
            mycursor.execute(query_all)
            myresult = mycursor.fetchall()
            # for x in myresult:
            #     print(x)
            print(f'Executed select(*) successfully for table_name: {table}')

    print('\n\n Moving to Selecting specific cols\n\n')

    for i in range(200):
        print(f"Iteration: {i + 1}")
        for table, columns in tables.items():
            # random set
            random_columns = random.sample(columns, random.randint(1, len(columns)))
            print(table)
            print(random_columns)
            quoted_columns = [f"`{col}`" for col in random_columns]
            query_random = f"SELECT {', '.join(quoted_columns)} FROM {table}"
            print(query_random)

            mycursor.execute(query_random)

            myresult = mycursor.fetchall()
            # for x in myresult:
            #     print(x)



schedule.every(1).minutes.do(execute_queries)

while True:
    schedule.run_pending()
    time.sleep(1)
