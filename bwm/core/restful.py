import os
import typing as t

from flask import Blueprint, current_app, request
from flask.scaffold import _sentinel
from flask_babel import lazy_gettext as _
from flask_restful import Api as _Api
from flask_restful import Resource as _Resource
from flask_restful import fields, marshal_with
from flask_restful.utils import OrderedDict, unpack
from werkzeug.wrappers import Response as ResponseBase

from bwm.util.permission import global_check_permission

try:
    from collections.abc import Mapping
except ImportError:
    from collections import Mapping


class Api(_Api):
    def handle_error(self, e):
        # 如果 flask 有自定义的错误处理,则还是由 flask 处理
        if current_app._find_error_handler(e):
            raise e
        return super().handle_error(e)


class Resource(_Resource):
    def dispatch_request(self, *args, **kwargs):

        # Taken from flask
        # noinspection PyUnresolvedReferences
        meth = getattr(self, request.method.lower(), None)
        if meth is None and request.method == "HEAD":
            meth = getattr(self, "get", None)
        assert meth is not None, "Unimplemented method %r" % request.method

        if isinstance(self.method_decorators, Mapping):
            decorators = self.method_decorators.get(request.method.lower(), [])
        else:
            decorators = self.method_decorators

        decorators = [global_check_permission] + list(decorators)
        for decorator in decorators:
            meth = decorator(meth)

        resp = meth(*args, **kwargs)

        if isinstance(resp, ResponseBase):  # There may be a better way to test
            return resp

        representations = self.representations or OrderedDict()

        # noinspection PyUnresolvedReferences
        mediatype = request.accept_mimetypes.best_match(representations, default=None)
        if mediatype in representations:
            data, code, headers = unpack(resp)
            resp = representations[mediatype](data, code, headers)
            resp.headers["Content-Type"] = mediatype
            return resp

        return resp

    def success(self, message: str = _("成功")):
        return {"message": message}


def create_route(
    name: str,
    import_name: str,
    static_folder: t.Optional[t.Union[str, os.PathLike]] = None,
    static_url_path: t.Optional[str] = None,
    template_folder: t.Optional[str] = None,
    url_prefix: t.Optional[str] = None,
    subdomain: t.Optional[str] = None,
    url_defaults: t.Optional[dict] = None,
    root_path: t.Optional[str] = None,
    cli_group: t.Optional[str] = _sentinel,  # type: ignore
    **api_kwargs: t.Any,
):
    bp = Blueprint(
        name=name,
        import_name=import_name,
        static_folder=static_folder,
        static_url_path=static_url_path,
        template_folder=template_folder,
        url_prefix=url_prefix,
        subdomain=subdomain,
        url_defaults=url_defaults,
        root_path=root_path,
        cli_group=cli_group,
    )
    api = Api(app=bp, **api_kwargs)
    return bp, api


def marshal_list(data: dict):
    return dict(data=fields.List(fields.Nested(data)), count=fields.Integer())


common_marshal = marshal_with({"message": fields.String()})
