from celery import Celery
from dotenv import load_dotenv
from flask import Flask

from .core import register

load_dotenv()

app = Flask(__name__, instance_relative_config=True)

register.register_components(
    app,
    [
        register.LogComponent,
        register.ConfigComponent,
        register.CORSComponent,
        register.SessionComponent,
        register.BcryptComponent,
        register.DBComponent,
        register.JWTComponent,
        register.BlueprintComponent,
        register.ErrorHandlerComponent,
        register.BabelComponent,
    ],
)

celery = Celery(__name__)
celery.config_from_object("celerytasks.celeryconfig")

__version__ = "0.1.0"
