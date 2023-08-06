import sys
import sys
from importlib import _bootstrap
from importlib.abc import MetaPathFinder
from types import ModuleType
from typing import Optional, Dict

from dataclasses import dataclass

from vim_quest_cli.deps.project2singleFile_export import ModuleDef, ModuleImporter

# True for both nodejs and browser.
IS_JS = sys.platform == "emscripten"

MODULES_TO_FAKE = ("termios", "curses", "curses.ascii", "importlib_resources")


def _module_def_from_name(module_name: str) -> ModuleDef:
    return ModuleDef(
        name=module_name,
        source="# Fake module",
        is_package=True,
        file=module_name.replace(".", "/") + ".py",
    )


def _create_fake_modules(modules_names=MODULES_TO_FAKE) -> None:
    modules = [_module_def_from_name(name) for name in modules_names]
    ModuleImporter.install(modules)


if IS_JS:
    sys.meta_path = sys.meta_path[:-1]
    _create_fake_modules()
