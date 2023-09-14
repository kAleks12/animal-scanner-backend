from uuid import UUID

from peewee import IntegrityError, DataError

from src.database.model.data.tag import Tag
from src.shared.exceptions import IntegrityException, InvalidDataException


def add(value: str, submission_id: UUID) -> Tag:
    try:
        return Tag.create(
            value=value,
            submission=submission_id
        )
    except IntegrityError as e:
        raise IntegrityException(str(e))
    except DataError as e:
        raise InvalidDataException(str(e))


def delete_for_submission(submission_id: UUID) -> Tag:
    try:
        return Tag.delete().where(Tag.submission == submission_id).execute()
    except IntegrityError as e:
        raise IntegrityException(str(e))
    except DataError as e:
        raise InvalidDataException(str(e))
