from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import DipData, SectorData


def get_sector_data(db: Session, sector_id: int) -> List[SectorData]:
    rows = []
    statement = select(SectorData).where(SectorData.sector_id.in_([sector_id]))
    for sector in db.scalars(statement):
        rows.append(sector)
    return rows


def get_dip_array(db: Session, ids: List[int]) -> List[DipData]:
    statement = select(DipData).where(DipData.id.in_(ids))
    dips = db.scalars(statement)
    return dips
