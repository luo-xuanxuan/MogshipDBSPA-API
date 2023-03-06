from loguru import logger
from mysql.connector import Error
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import get_settings


def create_connection():
    settings = get_settings()
    engine = None
    try:
        engine = create_engine(f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}")
        print("Connection to MySQL DB successful")
    except Error as e:
        print(e)
        logger.error(e)

    return engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


engine = create_connection()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
