import os

import click
from flask import Flask


def register_translate(app: Flask):
    @app.cli.group()
    def translate():
        """国际化命令"""

    @translate.command()
    def update():
        """更新所有语言"""
        if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
            raise RuntimeError("extract 报错")
        if os.system("pybabel update -i messages.pot -d bwm/translations"):
            raise RuntimeError("update 报错")
        os.remove("messages.pot")

    @translate.command()
    def compile():
        """编译所有语言"""
        if os.system("pybabel compile -d bwm/translations"):
            raise RuntimeError("compile 报错")

    @translate.command()
    @click.argument("lang")
    def init(lang: str):
        """新增新的语言"""
        if os.system("pybabel extract -F babel.cfg -k _l -o messages.pot ."):
            raise RuntimeError("extract 报错")
        if os.system(f"pybabel init -i messages.pot -d bwm/translations -l {lang}"):
            raise RuntimeError("init 报错")
        os.remove("messages.pot")
