from flask import current_app


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
