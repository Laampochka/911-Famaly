from services.db import Db


class Article():
    __tablename__ = 'articles'
    id = None
    author_id = None
    name = None
    text = None
    created_at = None

    def findAll(cls):
        db = Db()
        return db.query("SELECT * FROM 'articles'",{},cls)
        # print(items)