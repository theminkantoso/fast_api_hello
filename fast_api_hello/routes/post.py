from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.auth import JWTBearer
from config.database import get_db
from services.index import PostService

post = APIRouter(prefix="/v1/posts", tags=["Posts R routes"])


# @user.get("/", dependencies=[Depends(JWTRole())])
@post.get("", dependencies=[Depends(JWTBearer())])
async def get_all_posts():
    return PostService.get_all_posts()


@post.get("/owners")
async def get_all_posts_with_owners(db: Session = Depends(get_db)):
    return PostService.get_all_posts_with_owner(db)


@post.delete("/{id}")
async def delete_post(id: int):
    return PostService.delete_post(id)


