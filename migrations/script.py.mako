"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    # Preprocess
    pre_upgrade()

    ${upgrades if upgrades else "pass"}

    # Postprocess
    post_upgrade()


def downgrade():
    # Preprocess
    pre_downgrade()

    ${downgrades if downgrades else "pass"}

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
