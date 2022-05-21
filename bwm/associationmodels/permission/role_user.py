import sqlalchemy as sa

from bwm.registercomponent import db


class RoleUser(db.Model):
    """permission_role 和 account_user 的多对多中间表"""

    __tablename__ = "permission_role_user"

    role_id = sa.Column(sa.Integer, nullable=False, primary_key=True)
    user_id = sa.Column(sa.Integer, nullable=False, primary_key=True)
