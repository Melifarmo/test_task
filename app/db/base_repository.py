"""BaseRepository repository."""
from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    @property
    @abstractmethod
    def model(self) -> "Model":
        """Return repository model."""

    @property
    @abstractmethod
    def schema(self) -> "Schema":
        """Return model schema."""
