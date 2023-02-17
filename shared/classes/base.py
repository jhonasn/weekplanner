from peewee import SqliteDatabase as Database, Model, ForeignKeyAccessor, fn
from ..repository import db

class Base(Model):
    class Meta:
        database = db

    @classmethod
    def list(cls):
        return list(cls.select())

    @classmethod
    def count(cls):
        return cls.select(fn.COUNT(cls.id))
