from app.schemas.base_scheme import BaseSchema


class OrganisationPhone(BaseSchema):
    id: int
    phone: str
    organisation_id: int
