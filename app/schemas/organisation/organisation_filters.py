from typing import Any

from fastapi import Query
from pydantic import root_validator, ValidationError, Field

from app.schemas.base_scheme import BaseSchema
from app.schemas.organisation.rectangle_geo_search import RectangleGeoSearch


class OrganisationFilters(BaseSchema):
    building_id: int | None = Query(
        None,
        description="Look up organisation with linked building by its id",
    )
    activity_id: int | None = Query(
        None,
        description="Look up by specific activity id linked with organisation",
    )
    activity_name: str | None = Query(None, description="ilike linked activity title search")
    organisation_name: str | None = Query(None, description="ilike organisation title search")

    min_longitude: float | None = Query(
        None,
        description="look up organisation in geo rectangle. You must provide exactly 4 geo params or none of them",
    )
    max_longitude: float | None = Query(
        None,
        description="look up organisation in geo rectangle. You must provide exactly 4 geo params or none of them",
    )
    min_latitude: float | None = Query(
        None,
        description="look up organisation in geo rectangle. You must provide exactly 4 geo params or none of them",
    )
    max_latitude: float | None = Query(
        None,
        description="look up organisation in geo rectangle. You must provide exactly 4 geo params or none of them",
    )
    geo_rectangle: RectangleGeoSearch | None = Query(None, include_in_schema=False)

    @root_validator(pre=True)
    def organisation_filter_builder(cls, values: dict[str, Any]) -> dict[str, Any]:
        rect_values = [
            values.get('min_longitude'),
            values.get('max_longitude'),
            values.get('max_latitude'),
            values.get('min_latitude'),
        ]

        # если хотя бы один из 4 параметров передан
        if any(v is not None for v in rect_values):
            not_none_values = [v for v in rect_values if v is not None]
            if len(not_none_values) != 4:
                raise ValueError("You must provide exactly 4 geo params or none of them")

            values['geo_rectangle'] = cls._build_geo_rectangle(values)

        return values

    @classmethod
    def _build_geo_rectangle(cls, values: dict[str, Any]) -> RectangleGeoSearch:
        return RectangleGeoSearch(
            min_longitude=values['min_longitude'],
            max_longitude=values['max_longitude'],
            max_latitude=values['max_latitude'],
            min_latitude=values['min_latitude'],
        )
