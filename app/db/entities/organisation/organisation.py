from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, Table
from sqlalchemy.orm import relationship

from app.db.entities.base import Base


class OrganisationModel(Base):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=False)

    building_id = Column(
        Integer,
        ForeignKey("buildings.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    building = relationship(
        "BuildingModel",
        lazy="selectin",
    )
    phones = relationship(
        "OrganisationPhoneModel",
        lazy="selectin",
    )
