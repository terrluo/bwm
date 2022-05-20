from dotenv import load_dotenv
from flask import Flask

from . import registercomponent as register

load_dotenv()

app = Flask(__name__, instance_relative_config=True)

register.register_components(
    app,
    [
        register.LogComponent,
        register.ConfigComponent,
        register.DBComponent,
        register.JWTComponent,
        register.BlueprintComponent,
        register.ErrorHandlerComponent,
        register.BabelComponent,
    ],
)

__version__ = "0.1.0"
