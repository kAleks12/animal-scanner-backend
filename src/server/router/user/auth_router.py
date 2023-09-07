from fastapi import APIRouter, Depends

from src.server import get_error_responses
from src.server.model.user.user import UserLoginPayload, AuthResponse, UserRegisterPayload, ChangePasswordPayload
from src.service.user.auth_service import login, refresh_access, register, init_reset_password, logout, \
    reset_password, activate, change_password
from src.shared.enum.exception_info import ExceptionInfo
from src.utils.token_service import check_access_token, check_refresh_token, check_register_token, check_reset_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=AuthResponse,
             responses=get_error_responses([
                 ExceptionInfo.INVALID_CREDENTIALS,
                 ExceptionInfo.ENTITY_NOT_FOUND,
                 ExceptionInfo.USER_NOT_ACTIVE
             ]))
async def login_user(payload: UserLoginPayload):
    return AuthResponse(session=login(payload))


@router.post("/refresh", response_model=AuthResponse,
             responses=get_error_responses([
                 ExceptionInfo.TOKEN_EXPIRED,
                 ExceptionInfo.ENTITY_NOT_FOUND,
                 ExceptionInfo.INVALID_TOKEN
             ]))
async def refresh_user_access(val_payload=Depends(check_refresh_token)):
    return AuthResponse(session=refresh_access(val_payload[0], val_payload[1]))


@router.post("/change-password",
             responses=get_error_responses([
                 ExceptionInfo.TOKEN_EXPIRED,
                 ExceptionInfo.ENTITY_NOT_FOUND,
                 ExceptionInfo.USER_NOT_ACTIVE,
                 ExceptionInfo.INVALID_TOKEN
             ]))
async def change_user_password(payload: ChangePasswordPayload, token=Depends(check_access_token)):
    change_password(payload, token)


@router.post("/logout")
async def logout_user(token):
    logout(token)


@router.post("/register",
             responses=get_error_responses([
                 ExceptionInfo.USER_EXISTS
             ]))
async def register_user(payload: UserRegisterPayload):
    register(payload)


@router.post("/activate",
             responses=get_error_responses([
                 ExceptionInfo.ENTITY_NOT_FOUND,
                 ExceptionInfo.ALREADY_ACTIVE
             ]))
async def activate_user(token=Depends(check_register_token)):
    activate(token)


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
async def set_new_user_password(new_password: str, token=Depends(check_reset_token)):
    reset_password(token, new_password)
