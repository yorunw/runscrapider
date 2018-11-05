# -*-coding: utf8--*

from flask import Flask


def create_app():
    app = Flask(__name__)

    from .main import main
    app.register_blueprint(main, url_prefix='/')

    from .api import api
    app.register_blueprint(api, url_prefix='/api')

    return app
