import logging

from fastapi import HTTPException
from passlib.handlers.pbkdf2 import pbkdf2_sha512
from sqlalchemy import Row

from config.database import conn
from models.user import users


logger = logging.getLogger(__name__)
login_service_message = {"service_layer": "[login-service]"}
# logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
#                     format="[login-service] - %(asctime)s - %(levelname)s - %(message)s")


def get_user(email) -> Row | None:
    res = conn.execute(users.select().where(users.c.email == email)).first()
    if res is None:
        return None
    return res


def check_existed_then_get_user(email) -> dict:
    res = get_user(email)
    if res is None:
        logger.warning(f"User with email = {email} doesnt exist", extra=login_service_message)
        raise HTTPException(status_code=400, detail="Email or password wrong")
    user = convert_to_user(res)
    return user


def convert_to_user(user: Row) -> dict:
    user_data = user._data
    keys = ("id", "name", "email", "password", "role")
    return dict(zip(keys, user_data))


def user_password_check(user, password: str) -> bool:
    return pbkdf2_sha512.verify(password, user["password"])


class LoginService:
    @staticmethod
    def verify_user_and_get_info(email: str, password: str) -> dict:
        logger.info(f"Retrieving user with email = {email}", extra=login_service_message)
        user = check_existed_then_get_user(email)

        if not user_password_check(user, password):
            logger.warning(f"User with email = {email} sent a wrong password", extra=login_service_message)
            raise HTTPException(status_code=400, detail="Wrong password or email")

        return {"id": user["id"], "role": user["role"]}

    @staticmethod
    def get_user(email: str) -> Row:
        return get_user(email)

    @staticmethod
    def insert_user(new_user: dict):
        try:
            logger.info(f"Inserting user with email = {new_user['email']}", extra=login_service_message)
            new_user["role"] = 0
            new_user["password"] = pbkdf2_sha512.hash(new_user["password"])
            res = conn.execute(users.insert().values(new_user))
            conn.commit()
        except:
            logger.error(f"Error inserting user with email = {new_user['email']}, "
                          f"the insertion has been aborted",
                         extra=login_service_message)
            raise HTTPException(status_code=500, detail="Create user error")

    @staticmethod
    def user_existed(email: str) -> bool:
        user = get_user(email)
        print(user)
        if user is not None:
            return True
        return False


