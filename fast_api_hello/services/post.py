from fastapi import HTTPException
from sqlalchemy import Row, select

from config.database import conn
from models.index import posts
from models.user import users


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
        response = conn.execute(posts.select()).fetchall()
        return_dict = []

        for res in response:
            return_dict.append(convert_to_post(res))
        return return_dict

    @staticmethod
    def get_all_posts_with_owner() -> list[dict]:
        conn.commit()
        join_stmt = posts.join(users, posts.c.user_id == users.c.id)
        final_stmt = select(posts.c.topic, posts.c.content, users.c.name).select_from(join_stmt)
        response = conn.execute(final_stmt).fetchall()
        return_dict = []

        for res in response:
            return_dict.append(convert_to_post_owner(res))
        return return_dict

    @staticmethod
    def delete_post(id):
        try:
            conn.execute(posts.delete().where(posts.c.id == id))
            conn.commit()
        except:
            raise HTTPException(status_code=500, detail="Internal server error")


