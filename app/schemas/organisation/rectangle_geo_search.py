from pydantic import validator

from app.schemas.base_scheme import BaseSchema



class RectangleGeoSearch(BaseSchema):
    min_longitude: float
    max_longitude: float
    max_latitude: float
    min_latitude: float
