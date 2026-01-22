from fastapi.security.api_key import APIKeyHeader, APIKey
from fastapi import Security

from app.api.http_errors import ApiPermissionError
from app.settings import settings

api_key_header = APIKeyHeader(name=settings.API_KEY, auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)) -> APIKey:
    if api_key_header == settings.API_TOKEN:
        return api_key_header

    raise ApiPermissionError()



dependencies = [Security(get_api_key)],
