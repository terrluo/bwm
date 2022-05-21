from datetime import timedelta

import pytz

# flask-sqlalchemy
SQLALCHEMY_TRACK_MODIFICATIONS = False

# flask-jwt-extended
JWT_ERROR_MESSAGE_KEY = "message"
JWT_REVOKED_KEY = "revoked_token:{}"
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

# flask-babel
LANGUAGES = ["zh", "en"]
BABEL_DEFAULT_LOCALE = "zh"
BABEL_DEFAULT_TIMEZONE = "Asia/Shanghai"

# 自定义
LOCAL_TIMEZONE = pytz.timezone(BABEL_DEFAULT_TIMEZONE)
