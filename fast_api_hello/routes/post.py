import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.auth import JWTBearer
from config.database import get_db
from services.index import PostService

logger = logging.getLogger(__name__)
post_api_message = {"service_layer": "[post-api]"}
# logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
#                     format="post-api - %(asctime)s - %(levelname)s - %(message)s")
post = APIRouter(prefix="/v1/posts", tags=["Posts R routes"])


# @user.get("/", dependencies=[Depends(JWTRole())])
@post.get("", dependencies=[Depends(JWTBearer())])
async def get_all_posts():
    logger.info(msg="Fetching all posts in the system without owner")
    return PostService.get_all_posts()


@post.get("/owners")
async def get_all_posts_with_owners(db: Session = Depends(get_db)):
    logger.info(msg="Fetching all posts in the system", extra=post_api_message)
    return PostService.get_all_posts_with_owner(db)


@post.delete("/{id}")
async def delete_post(id: int):
    logger.warning(msg="Delete execution, removing post with id = {id}".format(id=id),
                   extra=post_api_message)
    return PostService.delete_post(id)


