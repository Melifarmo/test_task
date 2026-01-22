"""Create base tables

Revision ID: 5ecb68b667f5
Revises: 6971286c5f18
Create Date: 2024-08-19 16:16:20.062736

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""

import sqlalchemy as sa
from alembic import op

from app.db.migrations.id_column import IdColumn

revision = "5ecb68b667f5"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "activities",
        IdColumn(),
        sa.Column("title", sa.VARCHAR(), nullable=False),
        sa.Column("parent_id", sa.BIGINT()),
    )

    op.create_table(
        "buildings",
        IdColumn(),
        sa.Column("address", sa.VARCHAR(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
    )
    op.create_table(
        "organisation_phones",
        IdColumn(),
        sa.Column("phone", sa.VARCHAR(64), nullable=False),
        sa.Column("organisation_id", sa.BIGINT(), nullable=False),
    )

    op.create_table(
        "organisations",
        IdColumn(),
        sa.Column("title", sa.VARCHAR(), nullable=False),
        sa.Column("building_id", sa.BIGINT(), nullable=False),
    )
    # индексы особо не стал добавлять


def downgrade():
    op.drop_table("activities")
    op.drop_table("buildings")
    op.drop_table("organisation_phones")
    op.drop_table("organisations")
