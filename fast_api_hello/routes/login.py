import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import pbkdf2_sha512
from sqlalchemy import Row

from config.auth_handler import signJWT
from services.index import LoginService
from config.database import conn
from models.index import users
from schemas.login import Login
from schemas.index import RegUser

auth = APIRouter(prefix="/auth")


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
