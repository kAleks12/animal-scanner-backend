from peewee import CharField, BooleanField, BigAutoField, UUIDField

from src.database.model.user import UserBase


class User(UserBase):
    id = UUIDField(primary_key=True)
    username = CharField()
    password = CharField()
    email = CharField()
    refresh_token = CharField()
    activated = BooleanField()
    password_reset_code = CharField()
    activation_code = CharField()
