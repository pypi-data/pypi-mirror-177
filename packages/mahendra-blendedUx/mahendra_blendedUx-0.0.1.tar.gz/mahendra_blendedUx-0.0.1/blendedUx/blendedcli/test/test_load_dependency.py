import unittest
import os

from collections import OrderedDict

from blendedcli.backend import FileSystemBackend
from blendedcli.network import Network
from blendedcli.controller import Controller


theme_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_theme')



class TestLoadDependency(unittest.TestCase):
    def test_1(self):
        backend = FileSystemBackend(os.path.join(theme_dir, 'test_1'))
        expected_output = {
                            "meta": {
                                "config": {
                                    "palette": {
                                        "active": {
                                           "black": "#0e0000",
                                            "bold": "#724636",
                                            "bright": "#8a7256",
                                            "dark": "#3f2c20",
                                            "light": "#dfdad8",
                                            "very_dark": "#333333",
                                            "very_light": "#efeceb",
                                            "white": "#FFFFFF"
                                            },
                                        "fancy": {
                                            "colors": {
                                            "black": "#333333",
                                            "bold": "#4c1d59",
                                            "bright": "#f2ad85",
                                            "dark": "#3b1340",
                                            "light": "#f2b6b6",
                                            "very_dark": "#333333",
                                            "very_light": "#f2edd5",
                                            "white": "#CCCCCC"
                                            },
                                        "label": "Fancy"
                                        },
                                    "fdream": {
                                        "colors": {
                                            "black": "#000000",
                                            "bold": "#a12925",
                                            "bright": "#9e8d10",
                                            "dark": "#2d2214",
                                            "light": "#afab3f",
                                            "very_dark": "#333333",
                                            "very_light": "#8af0b7",
                                            "white": "#FFFFFF"
                                            },
                                        "label": "FuturisticDream"
                                        },
                                    "neutral": {
                                        "colors": {
                                            "black": "#0e0000",
                                            "bold": "#724636",
                                            "bright": "#8a7256",
                                            "dark": "#3f2c20",
                                            "light": "#dfdad8",
                                            "very_dark": "#333333",
                                            "very_light": "#efeceb",
                                            "white": "#FFFFFF"
                                            },
                                        "label": "Neutral"
                                            }
                                        }
                                    }
                                },

                            "html": {
                                    "home": "Hello User\n"
                                    }
                            }
        network = Network()
        controller = Controller(network, backend)
        package = dict(controller.get_package('theme_1', 'context'))
        package.pop('theme_name')
        # package = {}
        self.assertDictEqual.__self__.maxDiff = None
        self.assertDictEqual(package, dict(expected_output))
        

    def test_2(self):
        backend = FileSystemBackend(os.path.join(theme_dir, 'test_2'))
        expected_output = {
                            "css": {
                                "style": ".logo:before, .logo:after {\n\tcontent:'';\n\tdisplay:table;\n\tbox-sizing:border-box;\n}\n.logo:after {\n\tclear:both;\n}\n"
                            },
                            "palette": {
                                    "black": "#0e0000",
                                    "bold": "#724636",
                                    "bright": "#8a7256",
                                    "dark": "#3f2c20",
                                    "light": "#dfdad8",
                                    "very_dark": "#333333",
                                    "very_light": "#efeceb",
                                    "white": "#FFFFFF"
                            },
                            "template": {
                                    "home": "Hello World\n"
                            }
                        }

        network = Network()
        controller = Controller(network, backend)
        package = dict(controller.get_package('theme_3', 'context'))
        package.pop('theme_name')
        # package = {}
        self.assertDictEqual.__self__.maxDiff = None
        self.assertDictEqual(package, dict(expected_output))

    def test_3(self):
        backend = FileSystemBackend(os.path.join(theme_dir, 'test_3'))
        expected_output = {
                            "html": {
                                "wide": "This is Wide html\n",
                                "home": "Hello World\n"
                            },
                            "css": {
                                "style": ".logo:before, .logo:after {\n\tcontent:'';\n\tdisplay:table;\n\tbox-sizing:border-box;\n}\n.logo:after {\n\tclear:both;\n}\n"
                            },
                            "palette": {
                                "black": "#0e0000",
                                "bold": "#724636",
                                "bright": "#8a7256",
                                "dark": "#3f2c20",
                                "light": "#dfdad8",
                                "very_dark": "#333333",
                                "very_light": "#efeceb",
                                "white": "#FFFFFF"
                            },
                            "template": {
                                "wide": "This is Wide html\n",
                                "home": "Hello World\n"
                            }
                        }
        network = Network()
        controller = Controller(network, backend)
        package = dict(controller.get_package('theme_5', 'context'))
        package.pop('theme_name')
        # package = {}
        self.assertDictEqual.__self__.maxDiff = None
        self.assertDictEqual(package, dict(expected_output))

    def test_4(self):
        backend = FileSystemBackend(os.path.join(theme_dir, 'test_4'))
        expected_output = {
                    "meta": {
                        "config": {
                              "logo": {
                                    "text": "THEME 6",
                                    "image": "theme_6/media/logo.png",
                                    "alt": "Remodeling",
                                    "tag": "theme_6/media/logo.png",
                                    "title": "Theme new"
                                   }
                              }
                        },
                    "logo": "theme_7/media/logo.png"
                    }
        network = Network()
        controller = Controller(network, backend)
        package = dict(controller.get_package('theme_6', 'context'))
        package.pop('theme_name')
        #package = {}
        self.assertDictEqual.__self__.maxDiff = None
        self.assertDictEqual(package, dict(expected_output))

    def test_5(self):
        backend = FileSystemBackend(os.path.join(theme_dir, 'test_5'))
        expected_output = {
                            "html": {
                                "wide": "This is Wide html\n",
                                "home": "Hello World\n"
                            },
                            "css": {
                                "style": ".logo:before, .logo:after {\n\tcontent:'';\n\tdisplay:table;\n\tbox-sizing:border-box;\n}\n.logo:after {\n\tclear:both;\n}\n"
                            },
                            "logo": "Your Site",
                            "palette": {
                                "black": "#0e0000",
                                "bold": "#724636",
                                "bright": "#8a7256",
                                "dark": "#3f2c20",
                                "light": "#dfdad8",
                                "very_dark": "#333333",
                                "very_light": "#efeceb",
                                "white": "#FFFFFF"
                            },
                            "template": {
                                "wide": "This is Wide html\n",
                                "home": "Hello World\n"
                            }
                        }
        network = Network()
        controller = Controller(network, backend)
        package = dict(controller.get_package('theme_5', 'context'))
        package.pop('theme_name')
        #package = {}
        self.assertDictEqual.__self__.maxDiff = None
        self.assertDictEqual(package, dict(expected_output))

    def test_6(self):
        backend = FileSystemBackend(os.path.join(theme_dir, 'test_6'))
        expected_output = {
                            "html": {
                                "wide": "This is Wide html\n",
                                "home": "Hello World\n",
                                "left": "This is Sidebar html\n"
                            }
                        }
        network = Network()
        controller = Controller(network, backend)
        package = dict(controller.get_package('theme_6', 'context'))
        package.pop('theme_name')
        # package = {}
        self.assertDictEqual.__self__.maxDiff = None
        self.assertDictEqual(package, dict(expected_output))

    def test_7(self):
        backend = FileSystemBackend(os.path.join(theme_dir, 'test_7'))
        expected_output = {
                            "html": {
                                "wide": "This is Wide html\n",
                                "home": "Hello World\n",
                                "left": "This is Sidebar html\n"
                            },
                            "palette": {
                                "black": "#0e0000",
                                "bold": "#724636",
                                "bright": "#8a7256",
                                "dark": "#3f2c20",
                                "light": "#dfdad8",
                                "very_dark": "#333333",
                                "very_light": "#efeceb",
                                "white": "#FFFFFF"
                            },
                            'css': {
                                "style": ".logo:before, .logo:after {\n\tcontent:'';\n\tdisplay:table;\n\tbox-sizing:border-box;\n}\n.logo:after {\n\tclear:both;\n}\n"
                            },
                            "meta": {
                                "config": {
                                    "palette": {
                                        "active": {
                                            "black": "#0e0000",
                                            "bold": "#724636",
                                            "bright": "#8a7256",
                                            "dark": "#3f2c20",
                                            "light": "#dfdad8",
                                            "very_dark": "#333333",
                                            "very_light": "#efeceb",
                                            "white": "#FFFFFF"
                                        },
                                        "fancy": {
                                             "colors": {
                                                "black": "#333333",
                                                "bold": "#4c1d59",
                                                "bright": "#f2ad85",
                                                "dark": "#3b1340",
                                                "light": "#f2b6b6",
                                                "very_dark": "#333333",
                                                "very_light": "#f2edd5",
                                                "white": "#CCCCCC"
                                             },
                                        "label": "Fancy"
                                        },
                                        "fdream": {
                                            "colors": {
                                                "black": "#000000",
                                                "bold": "#a12925",
                                                "bright": "#9e8d10",
                                                "dark": "#2d2214",
                                                "light": "#afab3f",
                                                "very_dark": "#333333",
                                                "very_light": "#8af0b7",
                                                "white": "#FFFFFF"
                                            },
                                            "label": "FuturisticDream"
                                        },
                                        "neutral": {
                                            "colors": {
                                                "black": "#0e0000",
                                                "bold": "#724636",
                                                "bright": "#8a7256",
                                                "dark": "#3f2c20",
                                                "light": "#dfdad8",
                                                "very_dark": "#333333",
                                                "very_light": "#efeceb",
                                                "white": "#FFFFFF"
                                            },
                                            "label": "Neutral"
                                        }
                                    }
                                }
                            },
                            "stylesheets": {
                                "style": ".logo:before, .logo:after {\n\tcontent:'';\n\tdisplay:table;\n\tbox-sizing:border-box;\n}\n.logo:after {\n\tclear:both;\n}\n"
                            }
                        }
        network = Network()
        controller = Controller(network, backend)
        package = dict(controller.get_package('theme_7', 'context'))
        package.pop('theme_name')
        # package = {}
        self.assertDictEqual.__self__.maxDiff = None
        self.assertDictEqual(package, dict(expected_output))

    def test_8(self):
        backend = FileSystemBackend(os.path.join(theme_dir, 'test_8'))
        expected_output = {
                            "html": {
                                "wide": "This is Wide html\n",
                                "home": "Hello World\n",
                                "left": "This is Sidebar html\n"
                            },
                            "palette": {
                                "black": "#0e0000",
                                "bold": "#724636",
                                "bright": "#8a7256",
                                "dark": "#3f2c20",
                                "light": "#dfdad8",
                                "very_dark": "#333333",
                                "very_light": "#efeceb",
                                "white": "#FFFFFF"
                            }
                        }
        network = Network()
        controller = Controller(network, backend)
        package = dict(controller.get_package('theme_8', 'context'))
        package.pop('theme_name')
        # package = {}
        self.assertDictEqual.__self__.maxDiff = None
        self.assertDictEqual(package, dict(expected_output))


if __name__ == '__main__':
    unittest.main()