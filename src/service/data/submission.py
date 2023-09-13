import logging
import os
import uuid

from fastapi import UploadFile

from src.database.dal.data.submission import add, update, delete, get_one, get_all
from src.server.model.data.submission import SubmissionPayload, SubmissionDTO, SubmissionShortDTO, SubmissionLightDTO
from src.utils.config_parser import parser
from src.utils.utils import error_wrapper

logger = logging.getLogger("Submission_service")
upload_data_path = parser.get_attr("config", "upload_dir")

if not os.path.isdir(upload_data_path):
    os.mkdir(upload_data_path)


@error_wrapper(logger=logger)
def add_record(payload: SubmissionPayload, token_payload: dict) -> SubmissionLightDTO:
    record = add(token_payload["sub"], payload.x, payload.y, payload.description)
    return SubmissionLightDTO.from_orm(record)


@error_wrapper(logger=logger)
def edit_record(record_id: uuid, payload: SubmissionPayload) -> None:
    update(record_id, payload.x, payload.y, payload.description)


@error_wrapper(logger=logger)
def delete_record(record_id: uuid) -> None:
    delete(record_id)


@error_wrapper(logger=logger)
def get_single_record(record_id: uuid) -> SubmissionDTO:
    record = get_one(record_id)
    return SubmissionDTO.from_orm(record)


@error_wrapper(logger=logger)
def get_record_list() -> list[SubmissionShortDTO]:
    records = get_all()
    return [SubmissionShortDTO.from_orm(record) for record in records]


@error_wrapper(logger=logger)
def add_submission_photo(upload_file: UploadFile, submission_id: uuid.UUID):
    content = upload_file.file.read()
    full_path = upload_data_path + str(submission_id)
    with open(full_path, 'wb') as file:
        file.write(content)
