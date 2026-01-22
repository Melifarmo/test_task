from sqlalchemy import Column, Integer, VARCHAR, Float

from app.db.entities.base import Base


class BuildingModel(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    address = Column(VARCHAR, nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
