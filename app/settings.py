from pydantic.v1 import BaseSettings


class AppSettings(BaseSettings):
    POSTGRES_DSN: str

    API_KEY: str = "X-API-Key"
    API_TOKEN: str

    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = AppSettings()
