from fastapi import HTTPException
from passlib.handlers.pbkdf2 import pbkdf2_sha512
from sqlalchemy import Row

from config.database import conn
from models.user import users


def get_user(email) -> Row:
    res = conn.execute(users.select().where(users.c.email == email)).first()
    if res is None:
        return None
    return res


def check_existed_then_get_user(email) -> dict:
    res = get_user(email)
    if res is None:
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
        user = check_existed_then_get_user(email)

        if not user_password_check(user, password):
            raise HTTPException(status_code=400, detail="Wrong password or email")

        return {"id": user["id"], "role": user["role"]}

    @staticmethod
    def get_user(email: str) -> Row:
        return get_user(email)


    @staticmethod
    def insert_user(new_user):
        try:
            new_user["role"] = 0
            new_user["password"]= pbkdf2_sha512.hash(new_user["password"])
            res = conn.execute(users.insert().values(new_user))
            conn.commit()
        except:
            raise HTTPException(status_code=500, detail="Create user error")

    @staticmethod
    def user_existed(email: str) -> bool:
        user = get_user(email)
        print(user)
        if user is not None:
            return True
        return False


