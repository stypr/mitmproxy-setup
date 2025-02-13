#!/usr/bin/python3 -u

"""
Main script for mitmproxy
"""

import os
import pkgutil
import asyncio
import importlib

from mitmproxy import ctx, contentviews
from reloader import watch_changes, reload_modules

from views.sekai import ViewSekai
from addons.upstream_proxy import UpstreamProxy
from addons.web_console import WebConsole
from addons.no_cache import NoCache
from addons.debug import Debug

# Hot Reloading
for task in asyncio.all_tasks():
    if task.get_name() == 'watch_changes':
        ctx.log.info("Canceling previous autoreload task")
        task.cancel()
asyncio.create_task(watch_changes(), name="watch_changes")

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
    ViewSekai(),
]

# This code is required for adding/removing views
def load(loader):
    for view in views:
        contentviews.add(view)

def done():
    for view in views:
        contentviews.remove(view)
