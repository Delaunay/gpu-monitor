"""Top level module for gpusmi"""

import importlib
import pkgutil

__descr__ = "GPU monitoring utilities"
__version__ = "0.0.1"
__license__ = "BSD 3-Clause License"
__author__ = "Pierre Delaunay"
__author_email__ = "pierre@delaunay.io"
__copyright__ = "2022 Pierre Delaunay"
__url__ = "https://github.com/Delaunay/gpusmi"


def discover_plugins(module):
    """Discover uetools plugins"""
    path = module.__path__
    name = module.__name__

    plugins = {}

    for _, name, _ in pkgutil.iter_modules(path, name + "."):
        plugins[name] = importlib.import_module(name)
        print(f" - Found plugin: {name}")

    return plugins
