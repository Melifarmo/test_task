from app.schemas.base_scheme import BaseSchema


class Building(BaseSchema):
    id: int
    address: str
    longitude: str
    latitude: str
