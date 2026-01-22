from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.dependencies.db_session import get_session
from app.api.http_errors import EntityNotFound

from app.db.repo.organisation import OrganisationRepo

from app.schemas.organisation.organisation import Organisation
from fastapi import APIRouter, Depends, Request, Query

from app.schemas.organisation.organisation_filters import OrganisationFilters

organisation_router = APIRouter(
    prefix="/organisations",
)


@organisation_router.get(
    "/{organisation_id}",
    description="Get an organisation by organisation id",
    response_model=Organisation,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Organisation not found"},
    }
)
async def get_organisation_by_id(
    request: Request,
    organisation_id: int,
    db_session: AsyncSession = Depends(get_session),
) -> Organisation | None:
    repo = OrganisationRepo(db_session)  # Вообще, репозиторий должен браться из DI и использоваться UoW
    org = await repo.get(organisation_id)

    if not org:
        raise EntityNotFound("Organisation")

    return org


@organisation_router.get(
    "/",
    description="Get filtered organisations",
    response_model=list[Organisation],
    status_code=status.HTTP_200_OK,
)
async def get_organisations(
    request: Request,
    filters: Annotated[OrganisationFilters, Query()],
    db_session: AsyncSession = Depends(get_session),
) -> list[Organisation]:
    repo = OrganisationRepo(db_session)  # Вообще, репозиторий должен браться из DI и использовать UoW
    return await repo.get_all(
        organisation_name=filters.organisation_name,
        activity_id=filters.activity_id,
        building_id=filters.building_id,
        activity_name=filters.activity_name,
        geo_rectangle=filters.geo_rectangle,
    )
