import os
import pkgutil
import importlib

from pathlib import Path
from watchfiles import awatch, PythonFilter
from mitmproxy import ctx

# By default, Hot reloading is only done for Python scripts only
# Read https://watchfiles.helpmanual.io/api/filters/ for more information

class ReloadFilter(PythonFilter):
    ignore_paths = [os.path.realpath(__file__)]

async def watch_changes(trigger_file: Path):
    """
    Watch for all changes in the subdirectory
    the main script needs to be filtered as mitmproxy autoreloads main script changes
    """
    ctx.log.info("Autoreload task started")
    async for changes in awatch(
        os.path.dirname(os.path.realpath(__file__)),
        watch_filter=ReloadFilter()
    ):
        try:
            ctx.log.info(f"Changes detected: {changes}")
            trigger_file.touch()
        except Exception as e:
            print("Exception in autoreload:", e)

def reload_modules(module_dirs: list):
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
                    ctx.log.info(f"Reloading module: {module_name}")
                    importlib.reload(importlib.import_module(module_name))
        except ModuleNotFoundError as e:
            ctx.log.error(f"Reloading Module Error: {e}")
