
import sqlite3

class Db:
    def __init__(self):
        self.connection = sqlite3.connect('bd1')
        self.connection.row_factory = sqlite3.Row

    def query(self, sql, params={}, cls='' ):
        cursor = self.connection.cursor()
        row = cursor.execute(sql, params).fetchall()
        items = []
        for row in row:
            item_obj = cls()
            item = dict(row)
            for title, value in item.items():
                if hasattr(item_obj, title):
                    setattr(item_obj,title,value)

            items.append(item_obj)
        return items