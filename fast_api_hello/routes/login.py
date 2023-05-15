
from config.auth_handler import signJWT

from fastapi import APIRouter, Depends, HTTPException

from schemas.index import RegUser
from schemas.login import Login
from services.index import LoginService
from sqlalchemy import Row

auth = APIRouter(prefix="/v1/auth", tags=["Authenticate routes"])


@auth.post("/login")
async def login(login: Login):
    user_info = LoginService.verify_user_and_get_info(
        login.email, login.password
    )

    return signJWT(user_info["id"], user_info["role"])


@auth.post("/register")
async def reg_user(user: RegUser):
    new_user = {
        "name": user.name,
        "email": user.email,
        "password": user.password,
    }

    if LoginService.user_existed(user.email):
        raise HTTPException(status_code=400, detail="Email already existed")

    LoginService.insert_user(new_user)
    return {"msg": "register successful"}
