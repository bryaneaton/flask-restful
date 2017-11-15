import sqlite3
class ItemModel():

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name':self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        select_items = 'select name, price from items where name = ?'

        cursor = connection.cursor()
        result = cursor.execute(select_items, (name,))  # Single value Tuple
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row)

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "insert into items (price, name) Values(?,?)"
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()


    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "update items set price = ? where name = ?"
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()

    @classmethod
    def remove(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "delete from items where name = ?"
        cursor.execute(query, (item,))

        connection.commit()
        connection.close()

    @classmethod
    def retreiveMany(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "select name, price from items"
        result = cursor.execute(query)

        # TODO: retreive item list
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()

        return {'items': items}