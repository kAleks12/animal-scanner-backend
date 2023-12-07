import uuid

from fastapi import APIRouter, Depends, UploadFile, Query
from starlette.responses import FileResponse

from src.server import get_error_responses
from src.server.model.data.submission import SubmissionPayload, SubmissionDTO, SubmissionShortDTO, SubmissionLightDTO, \
    SubmissionEditPayload
from src.service.data.submission import add_record, edit_record, delete_record, get_single_record, get_record_list, \
    add_submission_photo, upload_data_path
from src.shared.enum.exception_info import ExceptionInfo
from src.utils.token_service import check_access_token

router = APIRouter(prefix="/submission", tags=["SubmissionRouter"])


@router.post("/", response_model=SubmissionLightDTO,
             responses=get_error_responses([
                 ExceptionInfo.TOKEN_EXPIRED,
                 ExceptionInfo.INVALID_TOKEN,
                 ExceptionInfo.INVALID_DATA,
                 ExceptionInfo.INTEGRITY_ERROR
             ]))
async def add_submission(payload: SubmissionPayload, token_payload=Depends(check_access_token)):
    return add_record(payload, token_payload)


@router.put("/{record_id}",
            responses=get_error_responses([
                ExceptionInfo.TOKEN_EXPIRED,
                ExceptionInfo.INVALID_TOKEN,
                ExceptionInfo.INVALID_DATA,
                ExceptionInfo.INTEGRITY_ERROR,
                ExceptionInfo.DOES_NOT_EXIST
            ]),
            dependencies=[Depends(check_access_token)])
async def update_submission(record_id: uuid.UUID, payload: SubmissionEditPayload):
    edit_record(record_id, payload)


@router.delete("/{record_id}",
               responses=get_error_responses([
                   ExceptionInfo.TOKEN_EXPIRED,
                   ExceptionInfo.INVALID_TOKEN,
                   ExceptionInfo.INVALID_DATA,
                   ExceptionInfo.INTEGRITY_ERROR,
                   ExceptionInfo.DOES_NOT_EXIST
               ]),
               dependencies=[Depends(check_access_token)])
async def delete_submission(record_id: uuid.UUID):
    return delete_record(record_id)


@router.get("/{record_id}", response_model=SubmissionDTO,
            responses=get_error_responses([
                ExceptionInfo.TOKEN_EXPIRED,
                ExceptionInfo.INVALID_TOKEN,
                ExceptionInfo.INVALID_DATA,
                ExceptionInfo.INTEGRITY_ERROR,
                ExceptionInfo.DOES_NOT_EXIST
            ]),
            dependencies=[Depends(check_access_token)])
async def get_submission_by_id(record_id: uuid.UUID):
    return get_single_record(record_id)


@router.get("/{record_id}/photo", response_model=SubmissionDTO,
            responses=get_error_responses([
                ExceptionInfo.TOKEN_EXPIRED,
                ExceptionInfo.INVALID_TOKEN,
                ExceptionInfo.INVALID_DATA,
                ExceptionInfo.INTEGRITY_ERROR,
                ExceptionInfo.DOES_NOT_EXIST
            ]),
            dependencies=[Depends(check_access_token)])
async def get_submission_photo(record_id: uuid.UUID):
    headers = {
        'Content-Disposition': f'attachment; filename:"{record_id}"',
        'Access-Control-Expose-Headers': 'Content-Disposition'
    }
    path = upload_data_path + str(record_id)
    media_type = 'image/jpeg'
    return FileResponse(path, headers=headers,media_type=media_type)


@router.get("/", response_model=list[SubmissionShortDTO],
            responses=get_error_responses([
                ExceptionInfo.TOKEN_EXPIRED,
                ExceptionInfo.INVALID_TOKEN,
                ExceptionInfo.INVALID_DATA,
                ExceptionInfo.INTEGRITY_ERROR,
                ExceptionInfo.DOES_NOT_EXIST
            ]),
            dependencies=[Depends(check_access_token)])
async def get_submissions():
    return get_record_list()


@router.post('/photo',
             responses=get_error_responses([
                 ExceptionInfo.TOKEN_EXPIRED,
                 ExceptionInfo.INVALID_TOKEN,
             ]),
             dependencies=[Depends(check_access_token)])
async def classify_image(file: UploadFile, sub_id: uuid.UUID = Query()):
    add_submission_photo(file, sub_id)
