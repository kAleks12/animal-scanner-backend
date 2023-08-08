from peewee import Model

from src.database.database import db_provider


def get_table_name(cls):
    return cls.__name__


class UserBase(Model):
    class Meta:
        database = db_provider.db
        table_function = get_table_name
        schema = "user"
