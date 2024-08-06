import mysql.connector
import random
import string
from datetime import datetime

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysql123",
    database="world"
)

mycursor = mydb.cursor()

tbl_lst = ["city", "country", "countrylanguage","lakecounty_health"]
tables = {}
for tbl in tbl_lst:
    query = f"SHOW COLUMNS FROM {tbl}"
    mycursor.execute(query)
    columns = mycursor.fetchall()
    column_names = [column[0] for column in columns]
    tables[tbl]=column_names
print(tables)

def get_random_string(length=10):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def get_random_int(min_value=1, max_value=100):
    return random.randint(min_value, max_value)

def get_distinct_values(table, column):
    query = f"SELECT DISTINCT {column} FROM {table}"
    mycursor.execute(query)
    result = mycursor.fetchall()
    return [row[0] for row in result]

def get_unique_value(table, column):
    existing_values_query = f"SELECT {column} FROM {table}"
    mycursor.execute(existing_values_query)
    existing_values = [row[0] for row in mycursor.fetchall()]

    while True:
        if isinstance(existing_values[0], int):
            new_value = get_random_int(1, 100000000)
        else:
            new_value = get_random_string()

        if new_value not in existing_values:
            return new_value

def find_constraints():
    primary_foreign_dict = {}
    for table, columns in tables.items():
        query = f"SELECT TABLE_NAME, COLUMN_NAME,\
                    CASE WHEN CONSTRAINT_NAME = 'PRIMARY' AND REFERENCED_COLUMN_NAME IS NULL THEN 'PRIMARY'\
                    WHEN CONSTRAINT_NAME != 'PRIMARY' AND REFERENCED_COLUMN_NAME IS NOT NULL THEN 'FOREIGN'\
                    END AS COL_TYPE\
                    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE \
                    where table_schema='{mydb.database}' and table_name='{table}' \
                    and (constraint_name='PRIMARY' or referenced_column_name is not NULL)"
        mycursor.execute(query)
        result = mycursor.fetchall()

        if table not in primary_foreign_dict:
            primary_foreign_dict[table] = {'pr_key': [], 'fr_key': []}

        for row in result:
            if row[2] == 'PRIMARY':
                primary_foreign_dict[table]['pr_key'].append(row[1])
            elif row[2] == 'FOREIGN':
                primary_foreign_dict[table]['fr_key'].append(row[1])
    return primary_foreign_dict

primary_foreign_keys = find_constraints()

def get_column_data_types(table):
    query = f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' AND TABLE_SCHEMA = '{mydb.database}'"
    mycursor.execute(query)
    result = mycursor.fetchall()
    return {row[0]: row[1] for row in result}

def make_random_changes():
    insert_counts = {table: {'inserted': 0, 'skipped': 0} for table in tables.keys()}

    for table, columns in tables.items():
        column_data_types = get_column_data_types(table)
        for _ in range(random.randint(10, 50)):
            values = []
            for column in columns:
                if column in primary_foreign_keys[table]['pr_key']:
                    new_value = get_unique_value(table, column)
                    values.append(new_value)
                elif column in primary_foreign_keys[table]['fr_key']:
                    distinct_values = get_distinct_values(table, column)
                    values.append(random.choice(distinct_values))
                else:
                    if column_data_types[column] in ['char', 'varchar', 'text']:
                        values.append(get_random_string())
                    elif column_data_types[column] in ['timestamp', 'datetime']:
                        values.append(datetime.now())
                    else:
                        values.append(get_random_int())

            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
            try:
                mycursor.execute(query, values)
                mydb.commit()
                insert_counts[table]['inserted'] += 1
            except mysql.connector.Error as err:
                retry_success = False
                if "Data too long" in str(err):
                    for scale in [10, 2]:
                        reduced_values = []
                        for i, column in enumerate(columns):
                            if column_data_types[column] in ['char', 'varchar', 'text']:
                                reduced_values.append(get_random_string(length=scale))
                            else:
                                reduced_values.append(get_random_int(min_value=1, max_value=scale))

                        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
                        try:
                            mycursor.execute(query, reduced_values)
                            mydb.commit()
                            insert_counts[table]['inserted'] += 1
                            retry_success = True
                            break
                        except mysql.connector.Error as retry_err:
                            continue

                elif "Duplicate entry" in str(err):
                    for _ in range(10):
                        new_values = values.copy()
                        for i, column in enumerate(columns):
                            if column in primary_foreign_keys[table]['pr_key']:
                                new_values[i] = get_unique_value(table, column)
                        try:
                            mycursor.execute(query, new_values)
                            mydb.commit()
                            insert_counts[table]['inserted'] += 1
                            retry_success = True
                            break
                        except mysql.connector.Error as final_err:
                            continue

                if not retry_success:
                    insert_counts[table]['skipped'] += 1

    print("Insert operation summary:")
    for table, counts in insert_counts.items():
        print(f"Table: {table} - Inserted: {counts['inserted']}, Skipped: {counts['skipped']}")

make_random_changes()
