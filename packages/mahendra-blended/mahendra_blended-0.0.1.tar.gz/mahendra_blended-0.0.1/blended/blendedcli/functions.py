from __future__ import absolute_import
import os
import re
import sys
from os.path import relpath
import hashlib
import jinja2
from blendedUxLang.blended.jinjaenv import BlendedEnvironment

from blended.blended_hostlib.controller import Controller
from blended.blended_hostlib.backend import FileSystemBackend
from blended.blended_hostlib.network import Network
from blended.blended_hostlib.exceptions import BlendedException
from blended.blended_hostlib.transform_image import TransformImage

from blended.blendedcli.settings import ROOT_DIR, IMAGE_CACHE_DIR, \
                                COMPILE_DIR, BLENDED_DIR, SRC
from blended.blendedcli.helpers import get_blended_directory_path, get_current_account
import blended.blendedcli.blendedUrls as blended_urls

try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin

CACHE_DIR = IMAGE_CACHE_DIR
src = os.path.join(BLENDED_DIR, SRC)


def multiple_replace(replace_characters, text):
    """
    """
    pattern = "|".join(map(re.escape, replace_characters.keys()))
    return re.sub(pattern, lambda m: replace_characters[m.group()], text)


def get_image_path(image_url, **kwargs):
    """
    Generate Cached Image.
    """
    replace_characters = {os.sep: '_', '.': '_'}
    filter_hash_char_replace = {'#': ''}
    filter_replace = {'series(': ''}
    height = kwargs.get('height', None)
    width = kwargs.get('width', None)
    filters = kwargs.get('filters', None)

    image_url = os.path.realpath(image_url)

    save_path = multiple_replace(replace_characters, image_url)

    file_extension = image_url.split('.')[-1].lower()

    if(height):
        save_path = '_'.join([save_path, str(height)])
    if(width):
        save_path = 'x'.join([save_path, str(width)])
    if(filters):
        save_path = '_'.join([save_path, str(filters)])
    if(file_extension):
        save_path = '.'.join([save_path, file_extension])

    save_path = multiple_replace(filter_hash_char_replace, save_path)
    save_path = os.path.join(CACHE_DIR, save_path)

    if(not os.path.exists(save_path)):
        obj = TransformImage(image_url, height, width)
        if(not filters):
            filters = 'series()'
        if(filters.startswith("series")):
            img_obj = obj.apply_filter(filters)
        else:
            # WHY this  TODO
            filters = multiple_replace(filter_replace, filters)
            # filters = filters.rstrip(")")
            img_obj = obj.apply_filter(filters)
            # img_obj = obj._do_series(filters)
        if file_extension:
            file_extension = file_extension.upper()
            if(file_extension == 'BMP'):
                extension = file_extension
            elif(file_extension == 'PNG'):
                extension = file_extension
            elif(file_extension == 'GIF'):
                extension = file_extension
            else:
                extension = 'JPEG'
            img_obj.image.save(save_path, extension, quality=100,
                               optimize=True, progressive=True)
    return save_path


def image(image_dict_obj, height=None, width=None, filters=None):
    """
    """
    if filters:
        if ((height == 0) or height) and ((width == 0) or width):
            pass
        elif not (height and width):
            print("Please pass height and width before using filters! error in:%s)" % image_dict_obj)
            sys.exit(0)
    elif height or width:
        filters = 'series(fill, crop(smart))'
    else:
        pass
    try:
        if height:
            float(height)
        if width:
            float(width)
    except ValueError:
        raise BlendedException("Please pass numerical value of height and width before using filters. "
                               "Default values are (0, 0)! error in:%s)" % image_dict_obj)
        sys.exit(0)
    try:
        relative_path = image_dict_obj.get('path')
        output = get_image_path(relative_path, height=height, width=width, filters=filters)
        url = "/media/%s" % (relpath(output, IMAGE_CACHE_DIR))
    except jinja2.exceptions.UndefinedError as exc:
        filename = exc.message.rsplit('attribute ')[1].replace("'", "")
        url = "/media/not_found/%s" % (filename)
    return url


def theme_data(theme_object, block, template):
    """
    using block and theme template,
    generates a dictionary that returns correct grid values from the theme object
    """
    template = '%s.html' % template
    grid_all = theme_object['theme']['meta']['grid']['all']
    block_all = theme_object['theme']['meta']['grid']['templates'][template]['all']
    block_dict = theme_object['theme']['meta']['grid']['templates'][template]['blocks'][block]
    grid_all.update(block_all)
    grid_all.update(block_dict)
    return grid_all


def nav_links(theme, template_name):
    """
    :param theme:
    :return:
    """
    blended_dir = get_blended_directory_path()
    current_account = theme.get('current_account')
    account = theme.get('account')
    path = theme.get('theme_path')
    version = theme.get('label')
    theme_name = theme.get('theme_name')
    account_path = os.path.join(blended_dir, current_account)
    relative_path = path.split(account_path)[1]
    if relative_path.startswith(os.sep):
        relative_path = relative_path.split(os.sep, 1)[1]
    if relative_path.endswith('lib'):
        relative_path = '%s/%s' % (relative_path, account)
    url = '/%s' % (template_name)
    return url


def generate_css_links(theme_object):
    """
    function to generate css file path dynamically.
    """
    blended_dir = get_blended_directory_path()
    urls = []
    network = Network()
    backend = FileSystemBackend()  # does backend take's compile directory path to initialize just for save_css call?
    current_account = get_current_account(network, network.get_user_pk())
    backend.directory_path = os.path.join(blended_dir, current_account)
    backend.current_account = current_account
    backend.blended_dir = blended_dir
    backend.blended_directory_path = blended_dir
    controller = Controller(network, backend)
    theme_name = theme_object.get('theme_name')
    css_path = theme_object.get('meta', {}).get('css', {})
    source_path = css_path.get('source', '')
    rendered_require = css_path.get('render_required')
    # compile_files = css_path.get('compile_targets')
    context = {'theme': dict(theme_object)}
    compiled_path = os.path.join(COMPILE_DIR, theme_name, 'css')

    for css_path in source_path:
        css_path = os.path.relpath(css_path)
        if css_path.endswith('.css'):
            css_file_path = css_path.rsplit('.css', 1)[0]
            splited_source_path = css_file_path.split(os.sep)
        else:
            splited_source_path = css_path.split(os.sep)

        if len(splited_source_path) > 0:
            css = content_at_source(splited_source_path, theme_object)

        if not css:
            try:
                # which directory will backend get initialize for ?
                if css_path.endswith('.css'):
                    css_file_path = css_path.rsplit('.css', 1)[0]
                    splited_source_path = css_file_path.split(os.sep)
                else:
                    splited_source_path = css_path.split(os.sep)
                theme_slug = splited_source_path.pop(0)
                try:
                    dependent_theme_object = controller.get_package(theme_slug, 'context')
                except (OSError, IOError):
                    print("failure in reading css from path %s" % (css_path))
            except BlendedException as exc:
                raise BlendedException(exc)
            css = content_at_source(splited_source_path, dependent_theme_object)

        if isinstance(css, str):
            file_path = os.path.join(compiled_path, css_file_path.rsplit(os.sep, 1)[-1])
            if(rendered_require):
                css = render_code(css, context)
            try:
                path = backend.save_css(file_path, css)
            except BlendedException as exc:
                raise BlendedException(exc)
            else:
                split_path = path.split(COMPILE_DIR)
                css_file_url = split_path[1]
                urls.append(css_file_url)
        else:
            urls = read_css_directory(css, compiled_path, rendered_require, urls, backend, context)

    return urls


def read_css_directory(css, compiled_path, rendered_require, urls, backend, context):
    """
    :param css:
    :param compile_path:
    :param rendered_require:
    :param urls:
    :return:
    """
    for each_file, file_content in css.items():
        file_path = os.path.join(compiled_path, each_file)
        if isinstance(file_content, dict):
            urls = read_css_directory(file_content, file_path, rendered_require, urls, backend, context)
        if (rendered_require):
            # css_content = env.from_string(file_content)
            file_content = render_code(file_content, context)

        try:
            path = backend.save_css(file_path, file_content)
        except BlendedException as exc:
            raise BlendedException(exc)
        else:
            split_path = path.split(COMPILE_DIR)
            css_file_url = split_path[1]
            urls.append(css_file_url)
    return urls


def render_code(file_content, context):
    """
    :param file_content: compiled template content
    :param context: theme_object or context
    :return: rendered content of template.
    """
    template = env.from_string(file_content)
    # with open("hello.txt", "w") as file_name:
    #     file_name.write(context)
    return template.render(context)


def content_at_source(splited_path_list, theme_object, directory_file={}):
    """
    :param splited_path_list:
    :param theme_object:
    :param directory_file:
    :return: directory_file
    """
    while(splited_path_list):
        index_value = splited_path_list.pop(0)
        theme_data = theme_object.get(index_value, {})
        if len(splited_path_list) > 0:
            directory_file = content_at_source(splited_path_list, theme_data, directory_file)
        else:
            if isinstance(theme_data, str):
                directory_file = theme_data
            else:
                directory_file.update(theme_data)

    return directory_file


def blended_hash(layout, prefix=None):
    if layout:
        try:
            hash_value = hashlib.md5(repr(layout.__dict__).encode('utf-8')).hexdigest()
            if prefix:
                prefix = prefix.replace(" ", "_")
                if (prefix[0].isalpha()) or (prefix[0] == '_'):
                    hash_value = prefix + hash_value
                else:
                    hash_value = "Prefix must start with 'alphabat' or '_'"
            else:
                hash_value = "layout_" + hash_value
        except Exception as e:
            hash_value = e
        return hash_value


def blended_home():
    """
    """
    # return 'http://localhost:8009/preview/src/yarnia_theme/templates/'
    return blended_urls.urlList[-1]

env = BlendedEnvironment()
env.globals.update({'css_links': generate_css_links,
                    'image': image,
                    'theme_data': theme_data,
                    'nav_links': nav_links,
                    'hash': blended_hash,
                    'home': blended_home
                    })

