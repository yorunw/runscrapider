# -*-coding: utf8-*-

from flask import Blueprint

api = Blueprint('api', __name__)

from . import routes
