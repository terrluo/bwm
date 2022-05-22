import sqlalchemy as sa

from bwm.util.component import get_db

_db = get_db()


class RoleUser(_db.Model):
    """permission_role 和 account_user 的多对多中间表"""

    __tablename__ = "permission_role_user"

    role_id = sa.Column(sa.Integer, nullable=False, primary_key=True)
    user_id = sa.Column(sa.Integer, nullable=False, primary_key=True)
