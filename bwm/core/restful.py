import os
import typing as t
from gettext import gettext

from flask import Blueprint
from flask.scaffold import _sentinel
from flask_restful import Api
from flask_restful import Resource as _Resource
from flask_restful import fields, marshal_with

_ = gettext


class Resource(_Resource):
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


common_marshal = marshal_with({"message": fields.String()})
