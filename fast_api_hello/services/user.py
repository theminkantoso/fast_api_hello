from fastapi import HTTPException
from sqlalchemy import Row

from config.database import conn
from models.user import users


def convert_to_user(user: Row):
    user_data = user._data
    keys = ("id", "name", "email", "password", "role")
    return dict(zip(keys, user_data))
class UserService:
    @staticmethod
    def get_all_users():
        res = conn.execute(users.select()).fetchall()
        ret = []
        for i in range(len(res)):
            ret.append(convert_to_user(res[i]))
        return ret

    @staticmethod
    def get_user_by_id(id):
        temp = conn.execute(users.select().where(users.c.id == id)).fetchall()
        return convert_to_user(temp[0])

    @staticmethod
    def update_user(id, user):
        try:
            conn.execute(users.update().values(
            name=user.name,
            email=user.email,
            password=user.password).where(users.c.id == id))

            conn.commit()
        except:
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    def delete_user(id):
        try:
            conn.execute(users.delete().where(users.c.id == id))
            conn.commit()
        except:
            raise HTTPException(status_code=500, detail="Internal server error")
