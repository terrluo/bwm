import sqlalchemy as sa
from sqlalchemy import text

from bwm.registercomponent import db


class BaseModel(db.Model):
    __abstract__ = True

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
        sa.SmallInteger, nullable=False, default=0, comment="是否删除 0否 1是"
    )

    class IsDelete:
        """是否删除"""

        NO = 0
        YES = 1
