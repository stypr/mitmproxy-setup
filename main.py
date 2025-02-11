#!/usr/bin/python3 -u

"""
Main script for mitmproxy
"""

import pkgutil
import logging
import importlib

from mitmproxy import contentviews
from views.pjsekai import ViewProjectSekai
from addons.upstream_proxy import UpstreamProxy
from addons.web_console import WebConsole
from addons.no_cache import NoCache
from addons.debug import Debug

# Hot Reloading
# If you want to reload everything, make changes to `main.py` or run `touch main.py`.
def reload_modules(module_dirs):
    """
    Reload all modules in subdirectories
    """
    for module_dir in module_dirs:
        try:
            package = importlib.import_module(module_dir)
            for _, module_name, is_pkg in pkgutil.walk_packages(
                package.__path__,
                module_dir + "."
            ):
                if not is_pkg:
                    logging.info("Reloading module: %s", module_name)
                    importlib.reload(importlib.import_module(module_name))
        except ModuleNotFoundError as e:
            logging.error("Error: %s", e)

reload_modules([
    "addons",
    "views"
])

# All addons go here
addons = [
    UpstreamProxy(),
    WebConsole(),
    NoCache(),
    Debug()
]

# All Views go here
views = [
    ViewProjectSekai(),
]

####
# This code is required for adding/removing views

def load(loader):
    for view in views:
        contentviews.add(view)

def done():
    for view in views:
        contentviews.remove(view)
