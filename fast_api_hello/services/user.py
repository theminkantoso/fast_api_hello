import logging

from fastapi import HTTPException
from sqlalchemy import Row

from config.database import conn
from models.user import users


logger = logging.getLogger(__name__)
user_service_message = {"service_layer": "[user-service]"}
# logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
#                     format="[user-service] - %(asctime)s - %(levelname)s - %(message)s")
def convert_to_user(user: Row):
    user_data = user._data
    keys = ("id", "name", "email", "password", "role")
    return dict(zip(keys, user_data))

class UserService:
    @staticmethod
    def get_all_users() -> list[dict]:
        logger.info("Getting all user in the system", extra=user_service_message)
        response = conn.execute(users.select()).fetchall()
        return_list = []
        for res in response:
            return_list.append(convert_to_user(res))
        return return_list

    @staticmethod
    def get_user_by_id(id) -> dict:
        logger.info(f"Getting user with id = {id}",
                    extra=user_service_message)
        temp = conn.execute(users.select().where(users.c.id == id)).fetchall()
        return convert_to_user(temp[0])

    @staticmethod
    def update_user(id, user):
        try:
            logger.info(f"Updating user with id = {id} with new values {user}",
                        extra=user_service_message)
            conn.execute(users.update().values(
            name=user.name,
            email=user.email,
            password=user.password).where(users.c.id == id))

            conn.commit()
        except:
            logger.error(f"Error updating user with id = {id} with new values {user}, aborting the update",
                         extra=user_service_message)
            raise HTTPException(status_code=500, detail="Internal server error")

    @staticmethod
    def delete_user(id):
        try:
            logger.info(f"Deleting user with id = {id}", extra=user_service_message)
            conn.execute(users.delete().where(users.c.id == id))
            conn.commit()
        except:
            logger.error(f"Error deleting user with id = {id} , aborting the deletion", extra=user_service_message)
            raise HTTPException(status_code=500, detail="Internal server error")
