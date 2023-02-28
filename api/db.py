from typing import List
from api.data import SectorData
from api.data import DipData
from mysql.connector import Error
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from loguru import logger

from api.settings import get_settings

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

def get_sector_data(sector_id: int) -> List[SectorData]:
    rows = []
    session = Session(create_connection())
    statement = select(SectorData).where(SectorData.sector_id.in_([sector_id]))
    for sector in session.scalars(statement):
        rows.append(sector)
    session.close()
    return rows

def get_dip_array(ids: List[int]) -> List[DipData]:
    session = Session(create_connection())
    statement = select(DipData).where(DipData.id.in_(ids))
    dips = session.scalars(statement)
    return dips