import time
from typing import List

from config.auth_handler import signJWT
from config.database import conn
from fastapi import APIRouter, Depends, HTTPException
from models.index import users
from passlib.hash import pbkdf2_sha512
from schemas.index import RegUser
from schemas.login import Login
from services.index import LoginService
from sqlalchemy import Row

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
