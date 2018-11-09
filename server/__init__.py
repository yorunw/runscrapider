# -*-coding: utf8-*-

from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    @app.route('/index', methods=['GET'])
    def index():
        """加载react-app"""
        return "index"

    from .api import api
    app.register_blueprint(api, url_prefix='/api')

    return app
