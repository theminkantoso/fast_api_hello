from sqlalchemy import Column, Integer, String, Table, ForeignKey

from config.database import meta, engine


posts = Table(
    'post', meta,
    Column('id', Integer, primary_key=True),
    Column('topic', String(255)),
    Column('content', String(255)),
    Column('user_id', Integer, ForeignKey("users.id"), nullable=False)
)

meta.create_all(engine)