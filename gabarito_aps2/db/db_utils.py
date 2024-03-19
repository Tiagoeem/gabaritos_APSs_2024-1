from db.db import *

# [1] referencia que utilizei para pegar as colunas do select = https://www.alixaprodev.com/how-to-get-column-names-from-sqlite-database-table-in-python/

def insert(table, columns, data):
    print(f"""INSERT INTO {table} ({", ".join(columns)}) VALUES ({", ".join(["%s"] * len(columns))});""")
    cursor.execute(f"""
    INSERT INTO {table} ({", ".join(columns)}) VALUES ({", ".join(["%s"] * len(columns))});
    """,data)

    conn.commit()

def select(table, columns = ["*"], condition = None):
    if (condition):
        cursor.execute(f"""SELECT {", ".join(columns)} FROM {table} WHERE {condition}""")
    else:
        cursor.execute(f"""SELECT {", ".join(columns)} FROM {table}""")

    columns = []
    for c in cursor.description: # [1]
        columns.append(c[0])

    rows_data = []

    for row in cursor.fetchall():
        dt = {}

        for i in range(len(columns)):
            dt[columns[i]] = row[i]

        rows_data.append(dt)

    return rows_data


def update(table, column, new_value, condition):
    print(column, new_value)
    if (condition):
        cursor.execute(f"UPDATE {table} SET {column} = '{new_value}' WHERE {condition}")
    else:
        cursor.execute(f"UPDATE {table} SET {column} = '{new_value}'")


    conn.commit()


def delete_by_id(table, id):
    cursor.execute(f"DELETE FROM {table} WHERE ID = {id}")
    conn.commit()