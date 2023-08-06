from __future__ import absolute_import
import os.path
import shutil
import pkgutil
import json
import configparser

from configparser import ConfigParser

import jinja2
from flask import Flask, Blueprint
from flask import request, render_template, send_from_directory
from werkzeug.exceptions import NotFound
from blendedUxLang.blended.jinjaenv import BlendedEnvironment

from blended.blended_hostlib.backend import FileSystemBackend
from blended.blended_hostlib.network import Network
from blended.blended_hostlib.controller import Controller

import blended.blendedcli.settings as settings

from blended.blendedcli.settings import ROOT_DIR, COMPILE_DIR, PREVIEWCACHEDCONTEXT
from blended.blendedcli.functions import render_code
from blended.blendedcli.helpers import get_blended_directory_path, get_current_account, resource_path

temp_compile = settings.COMPILE_DIR
USER_RC = settings.USER_RC
SRC = settings.SRC

try : 
    rc_file = resource_path(USER_RC)
    config = configparser.ConfigParser()
    config.read(rc_file)
    BLENDED_DIR = config.get("Directory", "directory_path")
    if BLENDED_DIR == '':
        BLENDED_DIR = settings.BLENDED_DIR
except:
    BLENDED_DIR = settings.BLENDED_DIR

src = os.path.join(BLENDED_DIR, SRC)
CACHE_DIR = settings.IMAGE_CACHE_DIR


# pkgutil code is hack for some python flask bug.
# you can go to this link 'https://github.com/pallets/flask/issues/1011#issuecomment-109494761' and see.
orig_get_loader = pkgutil.get_loader


def get_loader(name):
    try:
        return orig_get_loader(name)
    except AttributeError:
        pass
pkgutil.get_loader = get_loader

# theme_app = Blueprint('theme_app', __name__, template_folder=BLENDED_DIR)
theme_app = Flask(__name__, template_folder=src)
theme_object = {}


@theme_app.route('/<theme>/css/<filename>')
@theme_app.route('/<theme>/css/<path:path>/<filename>')
def send_css(**kwargs):
    filename = kwargs['filename']
    theme = kwargs['theme']
    path = kwargs.get('path')
    if not path:
        response = send_from_directory(os.path.join(COMPILE_DIR, theme, 'css'), filename, cache_timeout=1)
    elif path:
        response = send_from_directory(os.path.join(COMPILE_DIR, theme, 'css', path), filename, cache_timeout=1)
    return response


@theme_app.route('/media/<filename>')
@theme_app.route('/media/<path:path>/<filename>')
# @theme_app.route('/preview/<theme>/media/<filename>')
# @theme_app.route('/preview/<theme>/<template>/media/<filename>')
# @theme_app.route('/preview/<theme>/media/<path:path>/<filename>')
# @theme_app.route('/preview/<theme>/<template>/media/<path:path>/<filename>')
def send_media(**kwargs):
    filename = kwargs['filename']
    theme = kwargs.get('theme')
    path = kwargs.get('path')
    if (path):
        image_path = os.path.join(CACHE_DIR, path)
    else:
        image_path = os.path.join(CACHE_DIR)
    return send_from_directory(image_path, filename, cache_timeout=1)


@theme_app.route('/')
@theme_app.route('/<path:path>')
def base(version='blendeddefault', **kwargs):
    """
    """
    info = theme_app.client_info
    theme = info['package']
    account = None
    cached_context_file_name = theme
    if info["version"]:
        cached_context_file_name = info['account'] + theme + info['version']
        account = info['account']
        version = info["version"]
    network = Network()
    backend = FileSystemBackend()
    blended_dir = get_blended_directory_path()
    current_account = get_current_account(network, network.get_user_pk())
    blended_directory_path = os.path.join(blended_dir, current_account)
    backend.directory_path = blended_directory_path
    backend.current_account = current_account
    backend.blended_dir = blended_dir
    backend.blended_directory_path = blended_dir
    controller = Controller(network, backend)
    theme_name = theme
    query_string = request.query_string.decode('utf-8')
    # account_name = network.get_current_account(network.user_pk).slug
    if account:
        theme_directory = os.path.join(blended_directory_path, 'lib', account, theme_name)
    else:
        cached_context_file_name = current_account + theme + 'DRAFT'
        theme_directory = os.path.join(blended_directory_path, 'src', theme_name)

    temp_css_file_path = os.path.join(COMPILE_DIR, theme, 'css')
    original_css_path = os.path.join(theme_directory, 'css')
    if os.path.exists(original_css_path):
        try:
            shutil.copytree(original_css_path, temp_css_file_path)
        except OSError:
            shutil.rmtree(temp_css_file_path)
            shutil.copytree(original_css_path, temp_css_file_path)

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    if not os.path.exists(PREVIEWCACHEDCONTEXT):
        os.makedirs(PREVIEWCACHEDCONTEXT)
    if version and query_string:
        url = os.path.join(theme, version, query_string)
    elif version and not query_string:
        url = os.path.join(theme, version)
    elif not version and query_string:
        url = os.path.join(theme, query_string)
    else:
        url = os.path.join(theme)
    path = kwargs.get('path')
    context_object = {}
    try:
        if not info["no_caching"]:
            cached_context_file_path = PREVIEWCACHEDCONTEXT + os.sep + cached_context_file_name + '.json'
            if os.path.exists(cached_context_file_path):
                context_file_modification_time = os.path.getmtime(cached_context_file_path)
                if get_theme_modification_status(theme_directory, context_file_modification_time):
                    with open(cached_context_file_path, 'r') as openfile:
                        context_object = json.load(openfile)
    except OSError as e:
        pass

    if account:
        file_content, context = controller.preview(url, account=account, path=path, cached_context=context_object)
    else:
        file_content, context = controller.preview(url, path=path, cached_context=context_object)

    try:
        if not info["no_caching"]:
            json_object = json.dumps(context)
            # Writing to sample.json
            with open(PREVIEWCACHEDCONTEXT + os.sep + cached_context_file_name + '.json', "w") as outfile:
                outfile.write(json_object)
    except OSError as e:
        pass
    try:
        return render_code(file_content, context)
    except UnicodeDecodeError:
        return render_code(file_content.decode('utf-8'), context)


def get_theme_modification_status(theme_dir_root, cache_context_file_modification_time):
    """
    """
    for dirpath, dirnames, filenames in os.walk(theme_dir_root, topdown=True):
        if cache_context_file_modification_time < os.path.getmtime(dirpath):
            return False
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if cache_context_file_modification_time < os.path.getmtime(filepath):
                return False
    return True


def delete_css():
    try:
        shutil.rmtree(COMPILE_DIR)
    except OSError as e:
        pass

extra_dirs = [src, ]
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = os.path.join(dirname, filename)
            if os.path.isfile(filename):
                extra_files.append(filename)

delete_css()

if __name__ == '__main__':
    theme_app.run(host='0.0.0.0', debug=False, use_reloader=True, extra_files=extra_files)
