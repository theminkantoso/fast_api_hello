import time
from typing import List

from config.auth import JWTBearer
# from config.auth import JWTBearer
from config.database import conn
from config.role import JWTRole
from fastapi import APIRouter, Depends
from models.index import users
from pydantic import json
from schemas.index import RegUser, UpdateUser, User
from services.index import UserService
from sqlalchemy import Row

user = APIRouter(prefix="/v1/user", tags=["Users information CRUD routes"])


# @user.get("/", dependencies=[Depends(JWTRole())])
@user.get("", dependencies=[Depends(JWTBearer())])
async def get_all_user():
    return UserService.get_all_users()


@user.get("/{id}")
async def get_user_by_id(id: int):
    return UserService.get_user_by_id(id)


# @user.post("/", dependencies=[Depends(JWTRole(1))])
# async def write_data(user: RegUser):
#     new_user = {"name": user.name, "email": user.email, "password": user.password}
#     res = conn.execute(users.insert().values(new_user))
#     conn.commit()
#
#     result = conn.execute(users.select().where(users.c.id == res.lastrowid)).fetchall()
#     return convert_to_user(result[0])


@user.put("/{id}", dependencies=[Depends(JWTRole(1))])
async def update_user(id: int, user: UpdateUser):
    UserService.update_user(id, user)
    return UserService.get_user_by_id(id)


# @user.delete("/{id}", dependencies=[Depends(JWTRole(1))])
@user.delete("/{id}")
async def delete_user(id: int):
    UserService.delete_user(id)
    return {"msg": "Delete successful"}


