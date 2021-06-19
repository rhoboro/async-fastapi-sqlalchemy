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
    # 前処理
    pre_upgrade()

    pass

    # 後処理
    post_upgrade()


def downgrade():
    # 前処理
    pre_downgrade()

    pass

    # 後処理
    post_downgrade()


def pre_upgrade():
    # スキーマ更新前に実行する必要がある処理
    pass


def post_upgrade():
    # スキーマ更新後に実行する必要がある処理
    pass


def pre_downgrade():
    # スキーマ更新前に実行する必要がある処理
    pass


def post_downgrade():
    # スキーマ更新後に実行する必要がある処理
    pass
