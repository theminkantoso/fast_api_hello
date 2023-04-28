from sqlalchemy import Column, Integer, String, Table

from config.database import meta, engine


users = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('email', String(255)),
    Column('password', String(255)),
    Column('role', Integer))

meta.create_all(engine)
# from sqlalchemy import Column, Integer, String
#
# from config.database import Base
#
#
# class User(Base):
#     __tablename__='users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255))
#     email = Column(String(255))
#     password = Column(String(255))