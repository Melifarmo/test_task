from sqlalchemy import Column, Integer


class IdColumn(Column):
    def __new__(cls, *args, **kwargs):
        return Column(
            "id",
            Integer(),
            autoincrement=True,
            nullable=False,
            primary_key=True,
        )
