import sys
import os
import re
from os import path as opath
from importlib import import_module


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


class SpiderInfo:
    # SPIDER_DIR = './work/spiders/'
    PY_CACHE_DIR = '__pycache__'
    PY_INIT_FILE = '__init__.py'

    def __init__(self, spider_dir):
        self.base_dir = opath.abspath(spider_dir)
        self.path_list = []  # 类模块路径 type:list

        self.get_spider_path()
        sys.path.append(spider_dir)

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not hasattr(SpiderInfo, "_instance"):
            SpiderInfo._instance = object.__new__(cls)
        return SpiderInfo._instance

    def get_spider_path(self):
        for abs_path in self._get_spider_abs_path():
            self.path_list.append(_path2module(_split_base_dir(self.base_dir, abs_path)))
        return self.path_list

    def _get_spider_abs_path(self):
        """获取spider的绝对路径"""
        abs_path_list = []

        def _foo(parent_dir):
            """迭代文件夹获取路径"""

            for path in os.listdir(parent_dir):
                if path != self.PY_CACHE_DIR and path != self.PY_INIT_FILE:
                    abs_path = opath.join(parent_dir, path)

                    if opath.isdir(abs_path):
                        _foo(abs_path)

                    if opath.isfile(abs_path):
                        abs_path_list.append(abs_path)

        _foo(self.base_dir)
        return abs_path_list

    def import_module(self, path):
        module = import_module(path)
        return module


if __name__ == '__main__':
    s = SpiderInfo('./work/spiders/')
    # for path in s.path_list:
    #     print(path)
    #     m = s.import_module(path)
    #     print(dir(m))

    ss = SpiderInfo('./work/spiders')
    print(id(s))
    print(id(ss))

    # print(ss.path_list)
