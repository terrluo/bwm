from datetime import timedelta

# flask-sqlalchemy
SQLALCHEMY_ECHO = True

# flask-jwt-extended
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
