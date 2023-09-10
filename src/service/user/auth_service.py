import hashlib
import logging
from datetime import datetime, timedelta, timezone
from uuid import UUID

import pytz

from src.database.dal.user.user import get_login_user, get_by_id, get_by_email, add, \
    set_activation_code
from src.database.model.user.user import User
from src.server.model.user.user import UserLoginPayload, AuthSession, ChangePasswordPayload, UserRegisterPayload
from src.shared.exceptions import AuthException, GenericException, BadRequestException, NotFoundException
from src.utils.config_parser import parser
from src.utils.email_sender.sender import sender
from src.utils.token_service import generate_token, validate_token, generate_random_string, \
    generate_reset_token, generate_register_token
from src.utils.utils import error_wrapper

logger = logging.getLogger("Auth-Service")


@error_wrapper(logger=logger)
def login(payload: UserLoginPayload) -> (AuthSession, str, datetime):
    hashed_password = hashlib.sha512(payload.password.encode('utf-8')).hexdigest()
    try:
        user = get_login_user(payload.user, hashed_password)
    except NotFoundException as e:
        logger.exception(e)
        raise AuthException("INVALID_CREDENTIALS", "Invalid credentials provided")

    if not user.activated:
        logger.info(f"Failed to authenticate user {user.id}. Account is not activated")
        raise AuthException("INACTIVE_USER", "Please verify your email address.")

    return _generate_auth_session(user)


@error_wrapper(logger=logger)
def refresh_access(payload: dict, token: str) -> AuthSession:
    user = get_by_id(UUID(payload['sub']))
    if not user.refresh_token:
        logger.info(f"Failed to refresh access token for user {user.id}. Session was terminated")
        raise AuthException("SESSION_TERMINATED", "User is logged out")
    if user.refresh_token != token:
        logger.info(f"Failed to refresh access token for user {user.id}. Old refresh token")
        raise AuthException("Old refresh token provided")

    access_token = generate_token(str(user.id), 'access')
    return AuthSession(access_token=access_token)


@error_wrapper(logger=logger)
def change_password(payload: ChangePasswordPayload, token_payload: dict[str, str]) -> None:
    user = get_by_id(UUID(token_payload['sub']))
    hashed_password = hashlib.sha512(payload.current_password.encode('utf-8')).hexdigest()
    new_hashed_password = hashlib.sha512(payload.new_password.encode('utf-8')).hexdigest()

    if user.password != hashed_password:
        logger.info(f"Failed to change password for user {user.id}. Invalid current password")
        raise BadRequestException("Invalid password provided")
    if hashed_password == new_hashed_password:
        logger.info(
            f"Failed to change password for user {user.id}. New password is the same as the current password")
        raise BadRequestException("Password are the same")

    user.password = new_hashed_password
    user.save()


@error_wrapper(logger=logger)
def logout(token: str) -> None:
    payload = validate_token(token, 'refresh')
    user = get_by_id(UUID(payload['sub']))
    if user.refresh_token != token:
        logger.info(f"Failed to logout user {user.id}. Old refresh token")
        raise BadRequestException("Old refresh token")
    user.refresh_token = None
    user.save()


@error_wrapper(logger=logger)
def init_reset_password(email: str) -> None:
    user = get_by_email(email)

    if not user.activated:
        logger.info(f"Failed to reset password for user {user.id}. Account is not activated")
        raise AuthException("INACTIVE_USER", "Please verify your email address.")

    code = hashlib.sha512(generate_random_string().encode('utf-8')).hexdigest()
    exp_delta = int(parser.get_attr("auth", 'reset_token_exp_min'))

    token = generate_reset_token(str(user.id), code, exp_delta)
    user.password_reset_code = code
    user.save()
    sender.send_reset_password(email, token, exp_delta)


@error_wrapper(logger=logger)
def reset_password(payload: dict, new_password: str) -> None:
    user = get_by_id(UUID(payload['sub']))

    if user.password_reset_code != payload['code']:
        logger.info(f"Failed to reset password for user {user.id}. Invalid reset code")
        raise BadRequestException("Invalid reset code provided")

    new_password_hash = hashlib.sha512(new_password.encode('utf-8')).hexdigest()
    user.password = new_password_hash
    user.save()


@error_wrapper(logger=logger)
def register(payload: UserRegisterPayload):
    password_hash = hashlib.sha512(payload.password.encode('utf-8')).hexdigest()
    user = add(username=payload.username, email=payload.email, password=password_hash)
    code = hashlib.sha512(generate_random_string().encode('utf-8')).hexdigest()
    token = generate_register_token(str(user.id), code)

    set_activation_code(user.id, code)
    sender.send_register(user.email, token)


@error_wrapper(logger=logger)
def activate(token: dict) -> None:
    user = get_by_id(UUID(token['sub']))
    if user.activation_code == token['code']:
        user.activated = True
        user.activation_code = None
        user.save()


def _generate_auth_session(user: User) -> (AuthSession, str, int):
    access_token = generate_token(str(user.id), 'access')
    refresh_token = generate_token(str(user.id), 'refresh')
    user.refresh_token = refresh_token
    user.save()
    refresh_token_timeout = int(parser.get_attr("auth", 'refresh_token_exp_min')) * 60

    return AuthSession(access_token=access_token), refresh_token, refresh_token_timeout
