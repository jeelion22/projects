from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

import os

db_user_name = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PWD")

# database url
SQL_ALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{db_user_name}:{db_password}@localhost/fastapi"
)


# create a engine for responsible for sqlalchemy to connect database
engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

# to talk with database we create session
SessionLocal = sessionmaker(autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
