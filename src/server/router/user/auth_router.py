from fastapi import APIRouter, Depends

from src.server import get_error_responses
from src.server.model.user.user import UserLoginPayload, AuthResponse, UserRegisterPayload, ChangePasswordPayload
from src.service.user.auth_service import login, refresh_access, register_user, init_reset_password, logout, \
    reset_password, activate_user, change_password
from src.shared.enum.exception_info import ExceptionInfo
from src.utils.token_service import check_access_token, check_refresh_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthResponse,
             responses=get_error_responses([
                 ExceptionInfo.INVALID_CREDENTIALS,
                 ExceptionInfo.ENTITY_NOT_FOUND,
                 ExceptionInfo.USER_NOT_ACTIVE
             ]))
async def post_login(payload: UserLoginPayload):
    return AuthResponse(session=login(payload))


@router.post("/refresh", response_model=AuthResponse,
             responses=get_error_responses([
                 ExceptionInfo.TOKEN_EXPIRED,
                 ExceptionInfo.ENTITY_NOT_FOUND,
                 ExceptionInfo.INVALID_TOKEN
             ]))
async def post_refresh(token: str):
    return AuthResponse(session=refresh_access(token))


@router.post("/change-password",
             responses=get_error_responses([
                 ExceptionInfo.TOKEN_EXPIRED,
                 ExceptionInfo.ENTITY_NOT_FOUND,
                 ExceptionInfo.USER_NOT_ACTIVE,
                 ExceptionInfo.INVALID_TOKEN
             ]))
async def post_refresh(payload: ChangePasswordPayload, token=Depends(check_access_token)):
    change_password(payload, token)


@router.post("/logout")
async def post_logout(token):
    logout(token)


@router.post("/register",
             responses=get_error_responses([
                 ExceptionInfo.USER_EXISTS
             ]))
async def post_register(payload: UserRegisterPayload):
    register_user(payload)


@router.post("/activate",
             responses=get_error_responses([
                 ExceptionInfo.ENTITY_NOT_FOUND,
                 ExceptionInfo.ALREADY_ACTIVE
             ]))
async def post_activate(token: str):
    activate_user(token)


@router.post("/reset-password",
             responses=get_error_responses([
                 ExceptionInfo.ENTITY_NOT_FOUND,
                 ExceptionInfo.USER_NOT_ACTIVE
             ]))
async def post_reset_password(email: str):
    init_reset_password(email)


@router.post("/set-password",
             responses=get_error_responses([
                 ExceptionInfo.ENTITY_NOT_FOUND,
                 ExceptionInfo.INVALID_TOKEN,
                 ExceptionInfo.TOKEN_EXPIRED
             ]))
async def post_set_new_password(token: str, new_password: str):
    reset_password(token, new_password)
