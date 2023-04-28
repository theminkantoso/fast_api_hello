from typing import Optional

import uvicorn
from fastapi import FastAPI, Depends

from config.database import engine, SessionLocal
from routes.index import user
from routes.index import auth

# import models.user
# models.user.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user)
app.include_router(auth)

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