import logging

from fastapi import HTTPException
from sqlalchemy import Row, select

from config.database import conn, get_conn
from models.index import posts
from models.user import users


logger = logging.getLogger(__name__)
post_service_message = {"service_layer": "[post-service]"}
# logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
#                     format="[post-service] - %(asctime)s - %(levelname)s - %(message)s")

def convert_to_post(post: Row):
    post_data = post._data
    keys = ("id", "topic", "content", "user_id")
    return dict(zip(keys, post_data))


def convert_to_post_owner(post: Row):
    post_data = post._data
    keys = ("topic", "content", "poster_name")
    return dict(zip(keys, post_data))


class PostService:
    @staticmethod
    def get_all_posts() -> list[dict]:
        logger.info(msg="Querying post database to get all posts in the system", extra=post_service_message)
        response = conn.execute(posts.select()).fetchall()
        return_dict = []

        for res in response:
            return_dict.append(convert_to_post(res))
        return return_dict

    @staticmethod
    def get_all_posts_with_owner(db) -> list[dict]:
        logger.info(msg="Querying post database joining with the posts owner information",
                    extra=post_service_message)
        join_stmt = posts.join(users, posts.c.user_id == users.c.id)
        final_stmt = select(posts.c.topic, posts.c.content, users.c.name).select_from(join_stmt)

        # using yield db session object to query
        response = db.execute(final_stmt).fetchall()

        # using new method that generates new DB connection each time when invoked
        conn = get_conn()
        response = conn.execute(final_stmt).fetchall()
        conn.close()

        return_dict = []

        for res in response:
            return_dict.append(convert_to_post_owner(res))
        return return_dict

    @staticmethod
    def delete_post(id):
        try:
            logger.info("Service deleting posts with id = {id}".format(id=id), extra=post_service_message)
            conn.execute(posts.delete().where(posts.c.id == id))
            conn.commit()
        except:
            logger.error("Error in service deleting posts with id = {id}".format(id=id),
                         extra=post_service_message)
            raise HTTPException(status_code=500, detail="Internal server error")


