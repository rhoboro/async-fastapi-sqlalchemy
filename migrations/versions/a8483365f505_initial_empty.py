"""initial_empty

Revision ID: a8483365f505
Revises: 
Create Date: 2021-06-20 08:25:28.917425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a8483365f505"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Preprocess
    pre_upgrade()

    pass

    # Postprocess
    post_upgrade()


def downgrade():
    # Preprocess
    pre_downgrade()

    pass

    # Postprocess
    post_downgrade()


def pre_upgrade():
    # Processing before upgrading the schema
    pass


def post_upgrade():
    # Processing after upgrading the schema
    pass


def pre_downgrade():
    # Processing before downgrading the schema
    pass


def post_downgrade():
    # Processing after downgrading the schema
    pass
