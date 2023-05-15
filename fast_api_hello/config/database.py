from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@127.0.0.1:3306/fastapi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"connect_timeout": 5},
    pool_timeout=2,
    pool_recycle=2
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=True, )
#
Base = declarative_base()

meta = MetaData()

conn = engine.connect()
# conn = engine
