import sqlalchemy as sa
from sqlalchemy import text

from bwm.registercomponent import db


class IsType:
    NO = False
    YES = True


class BaseModel(db.Model):
    __abstract__ = True

    class IsDelete(IsType):
        """是否删除"""

    id = sa.Column(sa.Integer, primary_key=True)
    create_time = sa.Column(
        sa.TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="创建时间",
    )
    update_time = sa.Column(
        sa.TIMESTAMP,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        comment="更新时间",
    )
    is_delete = sa.Column(
        sa.Boolean, nullable=False, default=IsDelete.NO, comment="是否删除"
    )
