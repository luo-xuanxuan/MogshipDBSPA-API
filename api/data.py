from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class SectorData(Base):
    __tablename__ = "sector_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    uploader_version: Mapped[Optional[str]]
    return_time: Mapped[int]
    sector_id: Mapped[int]
    experience_rating: Mapped[int]
    discovered_sector_id: Mapped[int]
    is_first_time_explored: Mapped[bool]
    unlocked_submarine: Mapped[int]
    is_double_dip: Mapped[bool]
    favor_result: Mapped[int]
    experience: Mapped[int]
    surveillance: Mapped[int]
    retrieval: Mapped[int]
    favor: Mapped[int]
    dip_1: Mapped[int] = mapped_column(ForeignKey("dip_data.id"))
    dip_2: Mapped[Optional[int]] = mapped_column(ForeignKey("dip_data.id"))
    def __repr__(self) -> str:
        return ""

class DipData(Base):
    __tablename__ = "dip_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int]
    quantity: Mapped[int]
    is_hq: Mapped[bool]
    is_not_tier3: Mapped[bool]
    surveillance_result: Mapped[int]
    retrieval_result: Mapped[int]
    quality_result: Mapped[int]
    
    def __repr__(self) -> str:
        return ""
