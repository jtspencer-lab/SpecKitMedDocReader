"""Initial database schema migration template."""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial schema - populated when all models are complete."""
    pass


def downgrade() -> None:
    """Downgrade initial schema."""
    pass
