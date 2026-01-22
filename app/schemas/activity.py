from pydantic import Field

from app.constants import ACTIVITIES_MAP_LEVEL_DEEP
from app.db.entities import ActivityModel
from app.schemas.base_scheme import BaseSchema


class Activity(BaseSchema):
    id: int
    title: str

    parent_id: int | None = None
    children: list["Activity"] = Field(default_factory=list)

    @classmethod
    def from_entity(
        cls,
        entity: ActivityModel,
        level: int = 1,
        max_level: int = ACTIVITIES_MAP_LEVEL_DEEP,
    ) -> "Activity":
        activity = cls(
            id=entity.id,
            title=entity.title,
            parent_id=entity.parent_id,
            children=[],
        )

        if level >= max_level:
            return activity

        for child in entity.children:
            child_activity = cls.from_entity(
                child,
                level=level + 1,
                max_level=max_level,
            )
            activity.children.append(child_activity)

        return activity
