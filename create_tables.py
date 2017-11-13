import sqlite3


connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = 'create table IF NOT EXISTS users(id INTEGER primary key autoincrement, username text, password text)'

cursor.execute(create_table)

connection.commit()

connection.close()