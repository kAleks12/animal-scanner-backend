from peewee import UUIDField, DecimalField, ForeignKeyField, CharField, DateTimeField, BigAutoField

from src.database.model.data import DataBase
from src.database.model.data.submission import Submission
from src.database.model.user.user import User


class Tag(DataBase):
    id = BigAutoField()
    value = CharField()
    submission = ForeignKeyField(Submission, backref='tags')
