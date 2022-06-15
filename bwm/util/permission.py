from functools import wraps

from flask import _request_ctx_stack, current_app, request
from flask_jwt_extended import current_user


def global_check_permission(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if (
            getattr(_request_ctx_stack.top, "jwt", None) is not None
            and not getattr(func, "_skip_check_permission", False)
            and current_app.config.get("GLOBAL_PERMISSION_CHECK")
        ):
            current_user.check_permission(request.endpoint, request.method)
        return func(*args, **kwargs)

    return decorator


def check_permission(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if (
            not getattr(func, "_skip_check_permission", False)
            # 如果启用了全局的权限检查则不需要再次检查
            and not current_app.config.get("GLOBAL_PERMISSION_CHECK")
        ):
            current_user.check_permission(request.endpoint, request.method)
        return func(*args, **kwargs)

    return decorator


def skip_check_permission(func):
    func._skip_check_permission = True

    @wraps(func)
    def decorator(*args, **kwargs):
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
