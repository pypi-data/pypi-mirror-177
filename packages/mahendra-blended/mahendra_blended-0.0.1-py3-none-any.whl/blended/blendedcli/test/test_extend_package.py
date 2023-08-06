import unittest
import os

from collections import OrderedDict

from blendedcli.backend import FileSystemBackend
from blendedcli.network import Network
from blendedcli.controller import Controller


theme_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_theme', 'test_extend')


class TestExtendPackage(unittest.TestCase):
    def test_extend_1(self):
        """
        :return:
        """
        backend = FileSystemBackend(theme_dir)
        expected_output = [
            {'_project.json':
                 {
                  'slug': 'test_1_extend',
                  'description': 'test 1 is extended',
                  'dependencies': [
                         {
                          'alias': 'parent',
                          'account': None,
                          'slug': 'test_1'
                          }

                  ],

                  }
             },
            {'_index.json':
                 {
                  'meta':
                      {
                          '$ref': '@parent/meta'
                      },
                  'html':
                      {
                          '$ref': '@parent/html'
                      },
                  'palette': {
                      '$ref': '@parent/palette'
                  }
                 }
            }
        ]
        package = backend.get_package('test_1')
        backend.create_extended_package('test_1', package, 'test_1_extend', description='test 1 is extended')
        output = backend.get_package('test_1_extend')
        #print(output)
        self.maxDiff = None
        self.assertListEqual(expected_output, output)

    def test_extend_2(self):
        """
        :return:
        """
        backend = FileSystemBackend(theme_dir)
        expected_output = [
                            {
                             '_project.json': {
                                        'slug': 'test_2_extend',
                                        'description': 'test 2 is extended',
                                        'dependencies': [
                                                {
                                                'alias': 'parent',
                                                'slug': 'test_2',
                                                'account': None
                                                }
                                             ]
                                            }
                                },
                            {
                            '_index.json': {
                                    'meta': {
                                            '$ref': '@parent/meta'
                                        },
                                    'css': {
                                            '$ref': '@parent/css'
                                        },
                                    'palette': {
                                            '$ref': '@parent/palette'
                                        },
                                    'html': {
                                            '$ref': '@parent/html'
                                        },
                                    'template': {
                                            '$ref': '@parent/template'
                                        }
                                    }
                                }
            ]
        package = backend.get_package('test_2')
        backend.create_extended_package('test_2', package, 'test_2_extend', description='test 2 is extended')
        output = backend.get_package('test_2_extend')
        self.maxDiff = None
        self.assertListEqual(expected_output, output)


    def test_extend_resolve_2(self):
        """
        :return:
        """
        backend = FileSystemBackend(theme_dir)
        network = Network()
        controller = Controller(network, backend)
        expected_output = {
                            'html': {
                                'home': 'This is home for a package\n'
                                },

                            'css': {
                                'style': ".logo:before, .logo:after {\n\tcontent:'';\n\tdisplay:table;\n\tbox-sizing:border-box;\n}\n.logo:after {\n\tclear:both;\n}\n"
                                },
                            'meta': {
                                'config': {
                                    'palette': {
                                        'black': '#000000'
                                        }
                                    }
                                },
                            'palette': {
                                'black': '#000000'
                                },
                            'template': {
                                'home': 'This is home for a package\n'
                                }
                            }
        package = backend.get_package('test_2')
        backend.create_extended_package('test_2', package, 'test_2_extend', description='test 2 is extended')
        output = dict(controller.get_package('test_2_extend', 'context'))
        output.pop('theme_name')
        self.maxDiff = None
        self.assertDictEqual(expected_output, output)







if __name__ == '__main__':
    unittest.main()