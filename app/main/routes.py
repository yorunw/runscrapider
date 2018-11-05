# -*-coding: utf8--*

from . import main
from flask import render_template, url_for


@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/test-template-path')
def test_template_path():
    return render_template('main/index.html')


@main.route('/test-static-path')
def test_static_path():
    return url_for('main.static', filename='favicon.ico')
