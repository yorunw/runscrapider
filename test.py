import importlib
import re
import json
import sys
import os
from os import path as opath


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

    def __init__(self, base_dir, abs_path):
        """
        abs_path: /a/b/c/d
        base_dir: /a/b
        path: c/d
        module_path: c.d
        """
        self.base_dir = base_dir
        self.abs_path = abs_path
        self._path = ''
        self._module = None
        self._module_path = ''
        self._module_name = ''
        self._class_name = ''
        self._name = ''

    def load_module(self):
        self._module = importlib.import_module(self.module_path)

    def get_path(self):
        if self._path == '':
            self._path = _split_base_dir(self.base_dir, self.abs_path)
        return self._path

    path = property(get_path)

    def get_module_path(self):
        if self._module_path == '':
            if self._module is None:
                self.load_module()
            self._module_path = _path2module(self._path)
        return self._module_path

    module_path = property(get_module_path)

    def get_module_name(self):
        """spider所在的模块名"""

        if self._module_name == '':
            self._module_name = self._module_path.split('.')[-1]
        return self._module_name

    module_name = property(get_module_name)

    def get_class_name(self):
        """返回spider类名
        e.g.
            class DemoSpider(scrapy.Spider):
                name = 'demo'
                somecode...
        :return: DemoSpider -> str
        """
        if self._class_name != '':
            return self._class_name

        for attr in dir(self._module):
            if re.search('\w*?Spider$', attr):
                self._class_name = attr
        return self._class_name

    class_name = property(get_class_name)

    def get_name(self):
        """返回spider启动名
        e.g.
            class DemoSpider(scrapy.Spider):
                name = 'demo'
                somecode...
        :return: demo -> str
        """
        if self._name != '':
            return self._name

        cls = getattr(self._module, self._class_name)
        self._name = cls.name
        return self._name

    name = property(get_name)


class Spiders:
    PY_CACHE_DIR = '__pycache__'
    PY_INIT_FILE = '__init__.py'

    def __init__(self, spider_dir):
        self.base_dir = opath.abspath(spider_dir)  # spider目录
        self._abs_path_list = []  # spider绝对路径
        self._path_list = []  # spider相对路径

        sys.path.append(spider_dir)  # 将spider目录加入环境变量

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(Spider, "_instance"):
            Spider._instance = object.__new__(cls)
        return Spider._instance

    def _get_spider_abs_path(self):
        """获取spider的绝对路径"""

        def _foo(parent_dir):
            """迭代文件夹获取路径"""
            for path in os.listdir(parent_dir):
                if path != self.PY_CACHE_DIR and path != self.PY_INIT_FILE:
                    abs_path = opath.join(parent_dir, path)

                    if opath.isdir(abs_path):
                        _foo(abs_path)

                    if opath.isfile(abs_path):
                        self._abs_path_list.append(abs_path)

        _foo(self.base_dir)
        # return self._abs_path_list

    def load_path(self):
        if not self._abs_path_list:
            self._get_spider_abs_path()

        for abs_path in self._abs_path_list:
            path = _split_base_dir(self.base_dir, abs_path)
            self._path_list.append(path)

    def load_spider(self):
        pass

    def dump_json(self):
        temp_list = []

        def _foo(path, node):

            root, other = path.split('/', 1)

            if not node:
                x = {root: []}
                node.append(x)
                _foo(other, x[root])

            # else:
            #     for item in node:
            #         for i in item.keys():
            #             if root != i:
            #                 node.append({root: []})

            # _foo(other, root)

        for path in self._path_list:
            _foo(path, temp_list)

        print(temp_list)

    def load_json(self):
        pass


if __name__ == '__main__':
    pass
    s = Spiders('./work/spiders/')
    s.load_path()
    print(s._path_list)
    # s.dump_json()

"""
todo
lazy load:
init: spiders relation path
load a spider info
spider.json
"""
