# -*-coding: utf8-*-

import os
from os import path as op
import shutil

base_dir = op.abspath('..')

dist_dir = op.join(base_dir, 'view/build')
target_dir = op.join(base_dir, 'server')


def copy(dist_name, target_name):
    dist_path = op.join(dist_dir, dist_name)
    target_path = op.join(target_dir, target_name)

    if op.isfile(dist_path):
        if op.exists(target_path):
            os.remove(target_path)

        shutil.copyfile(dist_path, target_path)

    if op.isdir(dist_path):
        if op.exists(target_path):
            shutil.rmtree(target_path)

        shutil.copytree(dist_path, target_path)


def copy_static():
    static_list = os.listdir(op.join(dist_dir, 'static'))
    for item in static_list:
        copy('static/' + item, 'static/' + item)


copy('index.html', 'templates/index.html')
copy('favicon.ico', 'static/favicon.ico')
# copy('static/js', 'static/js')
# copy('static/css', 'static/css')
copy_static()
