import uuid

from peewee import IntegrityError, DataError, DoesNotExist

from src.database.model.data.submission import Submission
from src.database.model.user.user import User
from src.shared.exceptions import IntegrityException, InvalidDataException, BadRequestException


def add(user_id: uuid, x: float, y: float, description: str) -> Submission:
    try:
        return Submission.create(
            x=x,
            y=y,
            user=user_id,
            description=description
        )
    except IntegrityError as e:
        raise IntegrityException(str(e))
    except DataError as e:
        raise InvalidDataException(str(e))


def update(record_id: uuid, x: float, y: float, description: str) -> Submission:
    try:
        data = {
            Submission.x: x,
            Submission.y: y,
            Submission.description: description
        }
        return Submission.update(data).where(Submission.id == record_id).execute() == 1
    except IntegrityError as e:
        raise IntegrityException(str(e))
    except DataError as e:
        raise InvalidDataException(str(e))


def delete(record_id: uuid):
    try:
        Submission.delete_by_id(record_id)
    except IntegrityError as e:
        raise IntegrityException(str(e))
    except DataError as e:
        raise InvalidDataException(str(e))


def get_one(record_id: uuid):
    try:
        return (
            Submission.select(Submission, User)
            .left_outer_join(User, Submission.author)
            .where(Submission.id == record_id)
            .get()
        )
    except DoesNotExist as e:
        raise BadRequestException(str(e), "DOES_NOT_EXIST")


def get_all():
    return (
        Submission.select(Submission, User)
        .left_outer_join(User, Submission.author)
    )