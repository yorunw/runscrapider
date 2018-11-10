# -*-coding: utf8-*-

import os
from flask import Flask, render_template, send_from_directory


def create_app():
    app = Flask(__name__)

    @app.route('/')
    @app.route('/index')
    def index():
        """加载react-app"""
        return render_template('index.html')

    @app.route('/favicon.ico')
    def favicon():
        """将favicon.ico挂到跟路由下"""
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

    from .api import api
    app.register_blueprint(api, url_prefix='/api')

    return app
