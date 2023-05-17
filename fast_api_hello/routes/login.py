import logging
from config.auth_handler import signJWT

from fastapi import APIRouter, Depends, HTTPException
from schemas.index import RegUser
from schemas.login import Login
from services.index import LoginService

auth = APIRouter(prefix="/v1/auth", tags=["Authenticate routes"])
logger = logging.getLogger(__name__)
login_api_message = {"service_layer": "[login-api]"}
# logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
#                     format="[login-api] - %(asctime)s - %(levelname)s - %(message)s")

@auth.post("/login")
async def login(login: Login):
    user_info = LoginService.verify_user_and_get_info(
        login.email, login.password
    )
    logger.info(f"Log in user with email = {login.email} and password = {login.password}", extra=login_api_message)
    return signJWT(user_info["id"], user_info["role"])


@auth.post("/register")
async def reg_user(user: RegUser):
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": user.password,
    }
    logger.info(f"Register user with email = {login.email} and password = {login.password}", extra=login_api_message)
    if LoginService.user_existed(user.email):
        logging.warning(f"User with email = {login.email} already existed, abort the registration", extra=login_api_message)
        raise HTTPException(status_code=400, detail="Email already existed")

    LoginService.insert_user(new_user)
    return {"msg": "register successful"}
