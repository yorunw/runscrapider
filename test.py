import sys
import os
import re
from os import path as opath
import importlib


def _format_nt_path(path):
    """格式化windows路径为类unix格式"""

    path = re.sub(r'\w?:\\', '/', path)
    path = re.sub(r'\\', '/', path)
    return path


def _split_base_dir(base_dir, path):
    """去掉base_dir返回相对路径"""

    if os.name == 'nt':
        base_dir = _format_nt_path(base_dir)
        path = _format_nt_path(path)
    return re.sub(base_dir + '/', '', path)


def _path2module(path):
    """相对路径转换为类模块路径"""
    return re.sub(r'.py', '', re.sub('/', '.', path))


class Spider:

    def __init__(self, abs_path):
        """
        base_dir: /a/b
        abs_path: /a/b/c/d
        path: c/d
        module_path: c.d
        """
        self.base_dir = opath.abspath('./work/spiders/')
        self.abs_path = abs_path
        self.path = _split_base_dir(self.base_dir, self.abs_path)
        self.module_path = _path2module(self.path)
        self.class_name = self.get_spider_class_name()
        self.name = self.get_spider_name()

    @property
    def module(self):
        return importlib.import_module(self.module_path)

    def get_spider_class_name(self):
        """返回spider类名
        e.g.
            class DemoSpider(scrapy.Spider):
                name = 'demo'
                somecode...
        :return: DemoSpider -> str
        """
        for attr in dir(self.module):
            if re.search('\w*?Spider', attr):
                return attr

    def get_spider_name(self):
        """返回spider启动名
        e.g.
            class DemoSpider(scrapy.Spider):
                name = 'demo'
                somecode...
        :return: demo -> str
        """
        class_name = self.get_spider_class_name()
        cls = getattr(self.module, class_name)
        return cls.name


class Spiders:
    PY_CACHE_DIR = '__pycache__'
    PY_INIT_FILE = '__init__.py'

    def __init__(self, spider_dir):
        self.base_dir = opath.abspath(spider_dir)  # spider目录 str
        self.abs_path_list = []  # spider绝对路径 str
        self.spiders = []

        sys.path.append(spider_dir)  # 将spider目录加入环境变量

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(Spider, "_instance"):
            Spider._instance = object.__new__(cls)
        return Spider._instance

    def get_spider_abs_path(self):
        """获取spider的绝对路径"""

        def _foo(parent_dir):
            """迭代文件夹获取路径"""
            for path in os.listdir(parent_dir):
                if path != self.PY_CACHE_DIR and path != self.PY_INIT_FILE:
                    abs_path = opath.join(parent_dir, path)

                    if opath.isdir(abs_path):
                        _foo(abs_path)

                    if opath.isfile(abs_path):
                        self.abs_path_list.append(abs_path)

        _foo(self.base_dir)
        return self.abs_path_list

    def init_spider(self):
        for path in self.get_spider_abs_path():
            self.spiders.append(Spider(path))


if __name__ == '__main__':
    s = Spiders('./work/spiders/')
    s.init_spider()

    for spider in s.spiders:
        print(spider.name)
