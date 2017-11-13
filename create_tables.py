import sqlite3


connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_users = 'create table IF NOT EXISTS users(id INTEGER primary key autoincrement, username text, password text)'
create_items = 'create table if not exists items (id integer primary key AUTOINCREMENT , name text, price real)'


cursor.execute(create_users)
cursor.execute(create_items)

connection.commit()

connection.close()