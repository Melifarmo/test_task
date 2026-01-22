from fastapi import HTTPException


class AppBaseException(HTTPException):
    def __init__(self, *args, **kwargs):
        self.status_code = None
        self.detail = None


class EntityNotFound(AppBaseException):
    def __init__(self, entity_name: str):
        self.status_code = 404
        self.detail = f"{entity_name} not found"


class ApiPermissionError(AppBaseException):
    def __init__(self):
        self.status_code = 403
        self.detail = "permission denied"
