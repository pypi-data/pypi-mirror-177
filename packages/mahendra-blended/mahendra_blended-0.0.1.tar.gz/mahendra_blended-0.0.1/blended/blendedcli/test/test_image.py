import os
import unittest
from unittest import TestCase
from unittest.mock import patch

from PIL import Image

import blendedcli
from blendedcli.functions import image_2 as image
from blendedcli.settings import ROOT_DIR

image_path = 'images/test_image.jpg'

@patch('blendedcli.functions.src', '')
class TestTansformImage(TestCase):

    def test_image_simple_crop(self):
        '''
        :return:
        '''
        expected_height = 645
        expected_width = 1024
        url = image(image_path, filters='crop')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)

    def test_image_smart_crop(self):
        '''
        :return:
        '''
        expected_height = 345
        expected_width = 720
        url = image(image_path, expected_width, expected_height, filters='crop(smart)')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)

    def test_image_top_left_crop(self):
        '''
        :return:
        '''
        expected_height = 545
        expected_width = 720
        url = image(image_path, expected_width, expected_height, filters='crop(top-left)')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

    def test_image_center_crop(self):
        '''
        :return:
        '''
        expected_height = 545
        expected_width = 720
        url = image(image_path, expected_width, expected_height, filters='crop(center)')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

    def test_image_bottom_right_crop(self):
        '''
        :return:
        '''
        expected_height = 545
        expected_width = 720
        url = image(image_path, expected_width, expected_height, filters='crop(bottom-right)')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

    def test_image_fit(self):
        '''
        :return:
        '''
        expected_height = 452
        expected_width = 719
        url = image(image_path, 719, 454, filters='fit')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

    def test_image_fill(self):
        '''
        :return:
        '''
        expected_height = 452
        expected_width = 719
        url = image(image_path, 719, 450, filters='fill')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

    def test_image_fill_2(self):
        '''
        :return:
        '''
        expected_height = 452
        expected_width = 719
        url = image(image_path, 100, 100, filters="series(fill)")
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

    def test_image_fit_2(self):
        '''
        :return:
        '''
        expected_height = 452
        expected_width = 719
        url = image(image_path, 100, 100, filters='series(fit)')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

    def test_image_crop_1(self):
        '''
        :return:
        '''
        expected_height = 452
        expected_width = 719
        url = image(image_path, 100, 100, filters='series(crop(center))')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

    def test_image_fit_fil_2(self):
        '''
        :return:
        '''
        expected_height = 452
        expected_width = 719
        url = image(image_path, 100, 100, filters='series(fit, fill)')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

    def test_image_fit_crop_3(self):
        '''
        :return:
        '''
        expected_height = 452
        expected_width = 719
        url = image(image_path, 100, 100, filters='series(fit, crop(center))')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

    def test_image_fil_crop_3(self):
        '''
        :return:
        '''
        expected_height = 452
        expected_width = 719
        url = image(image_path, 100, 100, filters='series(fil, crop(center))')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

    def test_image_resize(self):
        '''
        :return:
        '''
        expected_height = 955
        expected_width = 1516
        url = image(image_path, 1220, 800, filters='resize')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width

        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

    def test_image_monochrome(self):
        '''
        :return:
        '''

        url = image(image_path, filters='monochrome')
        url = image(image_path, filters='monochrome(DDAA11)')
        url = image(image_path, filters='monochrome(#DDAA11)')
        url = image(image_path, filters='monochrome(DA1)')
        url = image(image_path, filters='monochrome(DDAA1111)')
        #path = os.path.join(ROOT_DIR, url)
        #with Image.open(path) as img:
         #   output_height = img.height
         #   output_width = img.width
        #self.assertEqual(output_width, expected_width)
        #self.assertEqual(output_height, expected_height)
        pass

    def test_image_alphachrome(self):
        '''
        :return:
        '''
        url = image(image_path, filters='alphachrome')
        url = image(image_path, filters='alphachrome(DDAA11)')
        url = image(image_path, filters='alphachrome(#DDAA11)')
        url = image(image_path, filters='alphachrome(DA1)')
        url = image(image_path, filters='alphachrome(DDAA1111)')
        pass

    def test_image_wrap(self):
        '''
        :return:
        '''
        url = image(image_path, filters='warp')
        pass

    def test_image_series(self):
        '''
        :return:
        '''
        expected_height = 452
        expected_width = 719
        url = image(image_path, 719, 452, filters='series(fit, fill, crop(center))')
        path = os.path.join(ROOT_DIR, url)
        with Image.open(path) as img:
            output_height = img.height
            output_width = img.width
        self.assertEqual(output_width, expected_width)
        self.assertEqual(output_height, expected_height)
        pass

#def image_2(relative_path, width=None, height=None, filters=None):
#    """
#    """
    #return relative_path

#    if not relative_path.startswith(src):
#        relative_path = os.path.relpath(relative_path)
#        relative_path = os.path.join(src, relative_path)
#    if (not filters):
#        filters = ''
#    output = get_image_path(relative_path, height=height, width=width, filters=filters)
    #print(relpath(output, ROOT_DIR))
#    url = "media/%s" % (relpath(output, IMAGE_CACHE_DIR))
    #return '/%s' % (relpath(output, ROOT_DIR))
#    return url

if __name__ == '__main__':
    unittest.main()
