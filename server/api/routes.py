# -*-coding: utf8-*-

from . import api
from flask.views import MethodView


class SpiderApi(MethodView):
    def get(self, id):
        if id is None:
            return "all"
        else:
            return str(id)

    def post(self, id):
        return id


spider_view = SpiderApi.as_view('spider_api')
api.add_url_rule('/spider/', defaults={'id': None}, view_func=spider_view, methods=['GET'])
api.add_url_rule('/spider/<int:id>', view_func=spider_view, methods=['GET'])
api.add_url_rule('/spider/<int:id>', view_func=spider_view, methods=['POST'])
