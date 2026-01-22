from fastapi import APIRouter, Security

from app.api.endpoints.api.operations_router import organisation_router
from app.apiUtils.authChecker import get_api_key

router = APIRouter(
    dependencies=[Security(get_api_key)],
    responses={403: {"details": "Permission denied"}},
)

router.include_router(organisation_router)
