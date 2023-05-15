from sqlalchemy import create_engine, MetaData, Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@127.0.0.1:3306/fastapi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"connect_timeout": 5},
    pool_timeout=2,
    pool_recycle=2
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine, expire_on_commit=True, )
Base = declarative_base()


# just declare to interact with old modules
meta = MetaData()

# engine.connect old method
conn = engine.connect()


def get_conn() -> Connection:
    """
    Generating new connection to interact with DB and fetch new data
    Instead of get all DB at once and not updating if no commit is made
    """
    return engine.connect()


def get_db() -> SessionLocal:
    """
    New yield session object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
