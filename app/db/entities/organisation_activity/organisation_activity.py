from sqlalchemy import Column, Integer, ForeignKey
from app.db.entities.base import Base


class OrganisationActivityModel(Base):
    __tablename__ = "organisation_activities"

    organisation_id = Column(
        Integer,
        ForeignKey("organisations.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    activity_id = Column(
        Integer,
        ForeignKey("activities.id", ondelete="RESTRICT"),
        primary_key=True,
        index=True,
    )
