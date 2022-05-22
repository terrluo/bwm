import uuid

import sqlalchemy as sa

from bwm.core.model import BaseModel, IsType
from bwm.util.component import get_bcrypt


class User(BaseModel):
    """用户"""

    __tablename__ = "account_user"

    class IsAdmin(IsType):
        """是否是管理员"""

    # 更新密码后需要重新生成 login_id
    login_id = sa.Column(sa.String(36), nullable=False, unique=True, comment="登录id")
    nickname = sa.Column(sa.String(16), nullable=False, unique=True, comment="昵称")
    username = sa.Column(sa.String(16), nullable=False, unique=True, comment="用户名")
    password = sa.Column(sa.String(60), nullable=False, comment="密码")
    is_admin = sa.Column(
        sa.Boolean, nullable=False, default=IsAdmin.NO, comment="是否是管理员, 管理员有所有权限"
    )

    def generate_login_id(self):
        return str(uuid.uuid4())

    def generate_password(self, password: str, rounds=None, prefix=None, bcrypt=None):
        return (
            self._get_bcrypt(bcrypt)
            .generate_password_hash(password, rounds=rounds, prefix=prefix)
            .decode("utf-8")
        )

    def check_password(self, password: str, bcrypt=None):
        return self._get_bcrypt(bcrypt).check_password_hash(self.password, password)

    def _get_bcrypt(self, bcrypt=None):
        return bcrypt if bcrypt else get_bcrypt()
