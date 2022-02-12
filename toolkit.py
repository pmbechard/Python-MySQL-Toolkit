import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter import ttk


def create_server_connection(host_name, user_name, user_password):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
        )
        print("MySQL Server connection successful")
    except Error as err:
        print(f"Error: '{err}'")
        return None
    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def create_database_connection(host_name, user_name, user_password, db_name):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
        return None
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def execute_list_query(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def show_table(connection, table):
    # TODO: Fix scrollbar issues
    query = f"""
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE 
        TABLE_SCHEMA = Database()
    AND TABLE_NAME = '{table}' ;
    """
    column_names = read_query(connection, query)

    query = f"""
    SELECT * FROM {table}
    """
    table_contents = read_query(connection, query)

    root = Tk()
    root.title(f"MySQL Database: {table}")

    canvas = Canvas(root)
    canvas.grid_propagate(False)
    canvas.grid(row=0, column=0)

    counter = 0
    for column_name in column_names:
        column_name = column_name[0].upper()
        ttk.Label(canvas, text=f'{column_name}', font=("Arial", 12, "bold")).grid(row=0, column=counter, padx=10, pady=10)
        counter += 1

    row_number = 1
    for row in table_contents:
        column_number = 0
        for column in row:
            ttk.Label(canvas, text=f'{column}', font=("Arial", 12)).grid(row=row_number, column=column_number, padx=10, pady=10)
            column_number += 1
        row_number += 1

    canvas.config(scrollregion=(0, 0, 1000, 1000))
    y_scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=canvas.yview)
    y_scrollbar.grid(row=0, column=1, sticky='ns')
    canvas.config(yscrollcommand=y_scrollbar.set)

    x_scrollbar = ttk.Scrollbar(root, orient=HORIZONTAL, command=canvas.xview)
    x_scrollbar.grid(row=1, column=0, sticky='ew')
    canvas.config(xscrollcommand=x_scrollbar.set)

    root.mainloop()
