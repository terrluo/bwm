from functools import wraps

from flask import current_app, request
from flask_jwt_extended import current_user


def check_permission(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if (
            # 如果启用了全局的权限检查则不需要再次检查
            not current_app.config.get("GLOBAL_PERMISSION_CHECK")
            and current_user is not None
        ):
            current_user.check_permission(request.endpoint, request.method)
        return func(*args, **kwargs)

    return decorator


def check_route_key(route_key: str):
    # 检查路由是否存在
    endpoint, method = unpack_route_key(route_key)
    rules = current_app.url_map.iter_rules(endpoint.lower())
    for rule in rules:
        if method.upper() not in rule.methods:
            raise KeyError
        break


def generate_route_key(endpoint: str, method: str):
    return f"{endpoint.lower()}#{method.upper()}"


def unpack_route_key(route_key: str):
    endpoint, method = route_key.split("#", 2)
    return endpoint, method
