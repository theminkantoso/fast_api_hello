from fastapi import Depends, FastAPI

from config.database import Base, engine
from routes.index import auth, user, post

from models import book

app = FastAPI()
app.include_router(user)
app.include_router(auth)
app.include_router(post)

Base.metadata.create_all(bind=engine)

#
# @app.get('/blog')
# def index(limit=10, published: bool = True, sort: Optional[str] = None):
#     print(published)
#     return {'data': f'{lzimit} publised blogs from the db'}
#
# @app.post('/blog')
# def post(request: Blog):
#     return request

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)