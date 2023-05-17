import logging

from config.auth import JWTBearer
from config.role import JWTRole
from fastapi import APIRouter, Depends

from schemas.index import RegUser, UpdateUser, User
from services.index import UserService

user = APIRouter(prefix="/v1/user", tags=["Users information CRUD routes"])


logger = logging.getLogger(__name__)
user_api_message = {"service_layer": "[user-api]"}
# logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
#                     format="[user-api] - %(asctime)s - %(levelname)s - %(message)s")

# @user.get("/", dependencies=[Depends(JWTRole())])
@user.get("", dependencies=[Depends(JWTBearer())])
async def get_all_user():
    logger.info("Controller calling to get all users in the system")
    return UserService.get_all_users()


@user.get("/{id}")
async def get_user_by_id(id: int):
    logger.info(f"Controller calling to get the user with id = {id} in the system",
                extra=user_api_message)
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
    logging.info(f"Controller calling to update the user with id = {id} in the system",
                 extra=user_api_message)
    UserService.update_user(id, user)
    return UserService.get_user_by_id(id)


# @user.delete("/{id}", dependencies=[Depends(JWTRole(1))])
@user.delete("/{id}")
async def delete_user(id: int):
    logging.info(f"Controller calling to delete the user with id = {id} in the system",
                 extra=user_api_message)
    UserService.delete_user(id)
    return {"msg": "Delete successful"}


