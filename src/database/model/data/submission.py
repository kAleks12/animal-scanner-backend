from peewee import UUIDField, DecimalField, ForeignKeyField, CharField

from src.database.model.data import DataBase
from src.database.model.user.user import User


class Submission(DataBase):
    id = UUIDField(primary_key=True)
    x = DecimalField()
    y = DecimalField()
    author = ForeignKeyField(User, null=True)
    filename = CharField()
    description = CharField(250)
