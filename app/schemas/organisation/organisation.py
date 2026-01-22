from app.schemas.activity import Activity
from app.schemas.base_scheme import BaseSchema
from app.schemas.building import Building
from app.schemas.organisation_phone import OrganisationPhone


class Organisation(BaseSchema):
    id: int
    title: str
    building_id: int

    building: Building
    phones: list[OrganisationPhone] = []
    activities: list[Activity] = []
