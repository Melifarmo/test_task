"""Create organisation activities

Revision ID: 1f927ea03430
Revises: 5ecb68b667f5
Create Date: 2026-01-20 17:48:30.420955

Doc: https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script
"""
from alembic import op
import sqlalchemy as sa


revision = '1f927ea03430'
down_revision = '5ecb68b667f5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organisation_activities",
        sa.Column("organisation_id", sa.Integer(), nullable=False),
        sa.Column("activity_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organisation_id"],
            ["organisations.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["activity_id"],
            ["activities.id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint(
            "organisation_id",
            "activity_id",
            name="pk_organisation_activities",
        ),
    )

    op.create_index(
        "ix_organisation_activities_organisation_id",
        "organisation_activities",
        ["organisation_id"],
    )
    op.create_index(
        "ix_organisation_activities_activity_id",
        "organisation_activities",
        ["activity_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_organisation_activities_activity_id",
        table_name="organisation_activities",
    )
    op.drop_index(
        "ix_organisation_activities_organisation_id",
        table_name="organisation_activities",
    )
    op.drop_table("organisation_activities")
