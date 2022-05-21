import typing as t
import uuid

import sqlalchemy as sa

from bwm.core.models import BaseModel
from bwm.registercomponent import bwm_bcrypt, db


class User(BaseModel):
    """用户"""

    __tablename__ = "account_user"

    # 更新密码后需要重新生成 login_id
    login_id = sa.Column(sa.String(36), nullable=False, unique=True, comment="登录id")
    nickname = sa.Column(sa.String(16), nullable=False, unique=True, comment="昵称")
    username = sa.Column(sa.String(16), nullable=False, unique=True, comment="用户名")
    password = sa.Column(sa.String(60), nullable=False, comment="密码")

    @classmethod
    def generate_login_id(cls):
        return str(uuid.uuid4())

    @classmethod
    def generate_password(cls, password: str, rounds=None, prefix=None):
        return bwm_bcrypt.generate_password_hash(
            password, rounds=rounds, prefix=prefix
        ).decode("utf-8")

    @classmethod
    def is_exist(cls, username: str):
        return db.session.query(
            User.query.filter_by(username=username).exists()
        ).scalar()

    @classmethod
    def get_active_user(cls, user_id: int) -> "t.Optional[User]":
        return User.query.filter(
            User.id == user_id,
            User.is_delete == User.IsDelete.NO,
        ).first()

    def check_password(self, password: str):
        return bwm_bcrypt.check_password_hash(self.password, password)
