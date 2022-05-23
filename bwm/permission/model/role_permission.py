import sqlalchemy as sa

from bwm.util.component import get_db

_db = get_db()


class RolePermission(_db.Model):
    """permission_role 和 permission_permission 的多对多中间表"""

    __tablename__ = "permission_role_permission"

    role_id = sa.Column(sa.Integer, nullable=False, primary_key=True)
    permission_id = sa.Column(sa.Integer, nullable=False, primary_key=True)
