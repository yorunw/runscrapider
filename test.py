import sys
import os
import re
from os import path
from importlib import import_module

SPIDER_DIR = './work/spiders/'
PY_CACHE_DIR = '__pycache__'
PY_INIT_FILE = '__init__.py'

sys.path.append(SPIDER_DIR)
base_dir = path.abspath(SPIDER_DIR)

'''
def spiders():
    for year_path in os.listdir(base_dir):
        year_abs_path = path.join(base_dir, year_path)
        if path.isdir(year_abs_path) and year_path != py_cache_dir:
            year_dir = year_abs_path
            print('year :', year_dir)

            for month_path in os.listdir(year_dir):
                month_abs_path = path.join(year_dir, month_path)
                if path.isdir(month_abs_path) and month_path != py_cache_dir:
                    month_dir = month_abs_path
                    print('month:', month_dir)

                    for date_path in os.listdir(month_dir):
                        date_abs_path = path.join(month_dir, date_path)
                        if path.isdir(date_abs_path) and date_path != py_cache_dir:
                            date_dir = date_abs_path
                            print('date :', date_dir)

                            for spider_path in os.listdir(date_dir):
                                spider = path.join(date_dir, spider_path)
                                if path.isfile(spider) and spider_path != py_init_file:
                                    spider = path.join(date_dir, spider_path)
                                    print('spider:', spider)

                                    yield spider
'''


def split_base_dir(abs_path):
    return re.sub(base_dir + '/', '', abs_path)

def path2module(path):
    return re.sub('/','.',path)

def bar():
    spiders = []

    def foo(parent_dir):
        for ppath in os.listdir(parent_dir):
            if ppath != PY_CACHE_DIR and ppath != PY_INIT_FILE:
                abs_path = path.join(parent_dir, ppath)

                if path.isdir(abs_path):
                    foo(abs_path)

                if path.isfile(abs_path):
                    spiders.append(split_base_dir(abs_path))

    foo(base_dir)
    return (spider for spider in spiders)


print(type(bar()))

for i in bar():
    i = path2module(i)
    print(i)

    # j = import_module(i)
    # print(j)
