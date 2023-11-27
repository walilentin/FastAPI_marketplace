from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'c199def8c4f9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}

    op.execute(
        """
    INSERT INTO role (name, role_permissions)
    VALUES
        ('GUEST', '["get_reviews", "view_site"]'),
        ('SELLER', '["create_product", "delete_product"]'),
        ('BUYER', '["buy_product", "add_review", "get_reviews"]'),
        ('ADMIN', '["manage_users", "manage_roles", "manage_products"]');
        """
    )

    # Additional upgrade statements for other tables if needed
    # ...


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}

    op.execute(
        """
        DELETE FROM role
        WHERE name IN ('GUEST', 'SELLER', 'BUYER', 'ADMIN');
        """
    )
