#!/usr/bin/python3 -u

"""
Main script for debugging
"""

import logging
import requests

from mitmproxy import contentviews
from views.sekai import ViewSekai
from addons.upstream_proxy import UpstreamProxy
from addons.web_console import WebConsole
from addons.no_cache import NoCache
from addons.debug import Debug

####

addons = [
    UpstreamProxy(),
    WebConsole(),
    NoCache(),
    Debug()
]

####

views = [
    ViewProjectSekai(),
]

####

def load(loader):
    for view in views:
        contentviews.add(view)

def done():
    for view in views:
        contentviews.remove(view)
