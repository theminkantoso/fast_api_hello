from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

from config.database import engine, Base



class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    book_title = Column(String(100))
    body = Column(String(100))


