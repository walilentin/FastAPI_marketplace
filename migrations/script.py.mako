"""${message}

ID ревізії: ${up_revision}
Переглядає: ${down_revision | comma,n}
Дата створення: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}

    op.execute(
        """
        INSERT INTO role (name, permissions)
        VALUES
            ('GUEST', '["get_reviews", "view_site"]'),
            ('SELLER', '["create_product", "delete_product"]'),
            ('BUYER', '["buy_product", "add_review", "get_reviews"]'),
            ('ADMIN', '["manage_users", "manage_roles", "manage_products"]');
        """
    )


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}


    op.execute(
        """
        DELETE FROM role
        WHERE name IN ('GUEST', 'SELLER', 'BUYER', 'ADMIN');
        """
    )
