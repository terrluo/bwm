import sqlalchemy as sa

from bwm.core.model import BaseModel


class Role(BaseModel):
    """角色"""

    __tablename__ = "permission_role"

    role_name = sa.Column(sa.String(32), nullable=False, comment="角色名称")
