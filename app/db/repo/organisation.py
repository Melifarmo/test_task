from collections import defaultdict
from typing import List, Optional, Tuple, Sequence

from sqlalchemy import select, Select
from sqlalchemy.orm import selectinload

from app.db.base_repository import BaseRepository
from app.db.entities import OrganisationActivityModel, ActivityModel, OrganisationModel, BuildingModel
from app.schemas.activity import Activity
from app.schemas.organisation.organisation import Organisation
from app.schemas.organisation.rectangle_geo_search import RectangleGeoSearch


class OrganisationRepo(BaseRepository):
    model = OrganisationModel
    schema = Organisation

    async def get(self, organisation_id: int) -> Optional[Organisation]:
        query = self._build_base_query()
        query = query.where(OrganisationModel.id == organisation_id)

        result = await self._session.execute(query)
        rows = result.all()  # TODO перевести на scalar?

        organisations = self._map_rows_to_schemas(rows)
        return organisations[0] if organisations else None

    async def get_all(
            self,
            activity_id: int | None = None,
            building_id: int | None = None,
            organisation_name: str | None = None,
            activity_name: str | None = None,
            geo_rectangle: RectangleGeoSearch | None = None,
    ) -> List[Organisation]:
        return await self._fetch_full_data(
            activity_id=activity_id,
            building_id=building_id,
            organisation_name=organisation_name,
            activity_name=activity_name,
            geo_rectangle=geo_rectangle,
        )

    async def _fetch_full_data(
            self,
            activity_id: int | None = None,
            building_id: int | None = None,
            organisation_name: str | None = None,
            activity_name: str | None = None,
            geo_rectangle: RectangleGeoSearch | None = None,
        ) -> List[Organisation]:
        query = self._build_base_query()

        if building_id:  # Если бы было не тестовое, то тут использовал бы паттерн "builder"
            query = query.where(OrganisationModel.building_id == building_id)
        if organisation_name:
            query = query.where(OrganisationModel.title.ilike(f"%{organisation_name}%"))
        if geo_rectangle:
            query = self._add_geo_rectangle_filter(query, geo_rectangle=geo_rectangle)
        if activity_id or activity_name:
            subquery = select(OrganisationActivityModel.organisation_id).join(ActivityModel)

            if activity_id:
                subquery = subquery.where(ActivityModel.id == activity_id)
            if activity_name:
                subquery = subquery.where(ActivityModel.title.ilike(f"%{activity_name}%"))
            query = query.where(OrganisationModel.id.in_(subquery))

        result = await self._session.execute(query)
        rows = result.all()

        return self._map_rows_to_schemas(rows)

    def _build_base_query(self) -> Select:
        return (
            select(OrganisationModel, ActivityModel)
            .outerjoin(
                OrganisationActivityModel,
                OrganisationActivityModel.organisation_id == OrganisationModel.id,
            )
            .outerjoin(ActivityModel, OrganisationActivityModel.activity_id == ActivityModel.id)
            .options(selectinload(ActivityModel.children))
        )

    def _add_geo_rectangle_filter(self, query, geo_rectangle: RectangleGeoSearch) -> Select:
        return (
            query.join(BuildingModel, BuildingModel.id == OrganisationModel.building_id)
            .where(BuildingModel.latitude.between(geo_rectangle.min_latitude, geo_rectangle.max_latitude))
            .where(BuildingModel.longitude.between(
                geo_rectangle.min_longitude,
                geo_rectangle.max_longitude,
            ))
        )

    def _map_rows_to_schemas(
            self,
            rows: Sequence[Tuple[OrganisationModel, Optional[ActivityModel]]]
    ) -> List[Organisation]:  # Не идеально, возникли проблемы с organisation.activies relationship, надо покопаться
        org_map = {}
        activities_map = defaultdict(list)

        for org, activity in rows:
            if org.id not in org_map:
                org_map[org.id] = org
            if activity:
                activities_map[org.id].append(activity)

        result: List[Organisation] = []
        for org in org_map.values():
            org_schema = self.schema.from_orm(org)
            org_schema.activities = [Activity.from_entity(a) for a in activities_map[org.id]]
            result.append(org_schema)
        return result
