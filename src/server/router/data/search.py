from fastapi import APIRouter, Depends

from src.server import get_error_responses
from src.server.model.data.search import PlaceDTO
from src.service.data.search_service import get_search_results
from src.shared.enum.exception_info import ExceptionInfo
from src.utils.token_service import check_access_token

router = APIRouter(prefix="/search", tags=["SearchRouter"])


@router.get("/", response_model=list[PlaceDTO],
            responses=get_error_responses([
                ExceptionInfo.TOKEN_EXPIRED,
                ExceptionInfo.INVALID_TOKEN
            ]),
            dependencies=[Depends(check_access_token)])
async def get_submission_by_id(query: str):
    return get_search_results(query)
