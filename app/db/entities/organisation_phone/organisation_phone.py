from sqlalchemy import Column, Integer, BigInteger, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from app.db.entities.base import Base


class OrganisationPhoneModel(Base):
    __tablename__ = "organisation_phones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone = Column(VARCHAR, nullable=False)
    organisation_id = Column(
        BigInteger,
        ForeignKey("organisations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    organisation = relationship(
        "OrganisationModel",
        back_populates="phones",
        lazy="joined",
    )
