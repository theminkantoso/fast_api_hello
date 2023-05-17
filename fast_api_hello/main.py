import logging

from fastapi import FastAPI

from config.database import Base, engine
from routes.index import auth, user, post

app = FastAPI()
app.include_router(user)
app.include_router(auth)
app.include_router(post)

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w",
                    format="%(service_layer)s - %(asctime)s - %(levelname)s - %(message)s")



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