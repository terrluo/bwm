import sqlalchemy as sa
from sqlalchemy import text

from bwm.type import Data
from bwm.util.component import get_db
from bwm.util.dt import to_local

_db = get_db()


class BaseModel(_db.Model):
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
    is_delete = sa.Column(sa.Boolean, nullable=False, default=False, comment="是否删除")

    @property
    def local_create_time(self):
        return to_local(self.create_time)

    @property
    def local_update_time(self):
        return to_local(self.update_time)

    def to_dict(self) -> Data:
        data = {}
        for column in self.__table__.columns:
            name: str = column.name
            data[name] = getattr(self, name)
        return data
