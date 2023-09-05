from uuid import UUID

from peewee import DoesNotExist, IntegrityError
from starlette import status

from src.database.model.user.user import User
from src.shared.exceptions import NotFoundException, InvalidDataException


def add(username, password, email) -> User:
    try:
        return User.create(
            username=username,
            password=password,
            email=email
        )
    except IntegrityError as e:
        raise InvalidDataException(str(e))


def update_user(user_id: UUID, new_password: str = None, new_username: str = None, new_email: str = None) -> None:
    try:
        user = User.get_by_id(user_id)
        changed = False
        if new_username is not None and new_username != user.username:
            user.username = new_username
            changed = True
        if new_email is not None and new_email != user.email:
            user.email = new_email
            user.activated = False
            changed = True
        if new_password is not None and new_password != user.__password:
            user.__password = new_password
            changed = True

        if changed:
            user.save()
    except DoesNotExist:
        raise NotFoundException("User does not exist")
    except IntegrityError as e:
        raise InvalidDataException(str(e))


def delete_user(user_id: UUID) -> None:
    try:
        user = User.get_by_id(user_id)
        user.delete_instance()
    except DoesNotExist:
        raise NotFoundException("User does not exist")


def get_login_user(email: str, password: str) -> User:
    try:
        return User.select(User).where(User.email == email, User.password == password)[0]
    except IndexError:
        raise NotFoundException("User does not exist")


def get_by_id(user_id: UUID) -> User:
    try:
        return User.get_by_id(user_id)
    except DoesNotExist:
        raise NotFoundException("User does not exist")


def get_by_email(email: str) -> User:
    try:
        return User.select(User).where(User.email == email)[0]
    except IndexError:
        raise NotFoundException("User does not exist")


def set_reset_password_code(user_id: UUID, code: str) -> None:
    try:
        user = User.get_by_id(user_id)
        user.password_reset_code = code
        user.save()
    except DoesNotExist:
        raise NotFoundException("User does not exist")


def set_activation_code(user_id: UUID, code: str) -> None:
    try:
        user = User.get_by_id(user_id)
        user.activation_code = code
        user.save()
    except DoesNotExist:
        raise NotFoundException("User does not exist")


def activate_user(user_id: UUID, token: str) -> None:
    try:
        user = User.get_by_id(user_id)
        if user.reset_email_token == token:
            user.activated = True
            user.save()
        else:
            raise InvalidDataException("Invalid token")
    except DoesNotExist:
        raise NotFoundException("User does not exist")