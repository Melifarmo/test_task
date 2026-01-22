from sqlalchemy import String, ForeignKey, BigInteger, Column
from sqlalchemy.orm import relationship

from app.constants import ACTIVITIES_MAP_LEVEL_DEEP
from app.db.entities.base import Base

class ActivityModel(Base):
    __tablename__ = "activities"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    parent_id = Column(
        BigInteger,
        ForeignKey("activities.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    children = relationship("ActivityModel", lazy="subquery", join_depth=ACTIVITIES_MAP_LEVEL_DEEP)
