import uuid
from datetime import date

from peewee import IntegrityError, DataError, DoesNotExist, prefetch

from src.database.model.data.submission import Submission
from src.database.model.data.tag import Tag
from src.database.model.user.user import User
from src.shared.exceptions import IntegrityException, InvalidDataException, BadRequestException


def add(user_id: uuid, x: float, y: float, description: str, relevant_date: date) -> Submission:
    try:
        return Submission.create(
            x=x,
            y=y,
            author=user_id,
            description=description,
            date=relevant_date
        )
    except IntegrityError as e:
        raise IntegrityException(str(e))
    except DataError as e:
        raise InvalidDataException(str(e))


def update(record_id: uuid, x: float, y: float, description: str, relevant_date: date) -> Submission:
    try:
        data = {
            Submission.x: x,
            Submission.y: y,
            Submission.description: description,
            Submission.date: relevant_date
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
        return prefetch(
            Submission.select(Submission, User)
            .left_outer_join(User, Submission.author)
            .where(Submission.id == record_id)
            .prefetch(Tag)[0]
        )
    except DoesNotExist as e:
        raise BadRequestException(str(e), "DOES_NOT_EXIST")


def get_all():
    return (
        Submission.select(Submission.id, Submission.x, Submission.y)
    )
