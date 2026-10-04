"""add asset kpis

Revision ID: 0ed6551ee5cf
Revises: 2f5eae99f12f
Create Date: 2026-10-04 22:07:07.891317

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ed6551ee5cf'
down_revision: Union[str, Sequence[str], None] = '2f5eae99f12f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "asset_kpis",
        sa.Column(
            "kpi_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("run_id", sa.BigInteger(), nullable=False),
        sa.Column("asset_id", sa.BigInteger(), nullable=False),

        sa.Column("asset_health_score", sa.Numeric(), nullable=True),
        sa.Column("operating_performance_index", sa.Numeric(), nullable=True),
        sa.Column("reliability_consequence_index", sa.Numeric(), nullable=True),

        sa.Column("load_index", sa.Numeric(), nullable=True),
        sa.Column("production_index", sa.Numeric(), nullable=True),
        sa.Column("downtime_30d_h", sa.Numeric(), nullable=True),
        sa.Column("emission_intensity_proxy", sa.Numeric(), nullable=True),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["asset_id"],
            ["core.assets.asset_id"],
        ),
        sa.ForeignKeyConstraint(
            ["run_id"],
            ["analytics.analysis_runs.run_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("kpi_id"),
        sa.UniqueConstraint(
            "run_id",
            "asset_id",
            name="uq_asset_kpis_run_asset",
        ),
        schema="analytics",
    )


def downgrade() -> None:
    op.drop_table("asset_kpis", schema="analytics")