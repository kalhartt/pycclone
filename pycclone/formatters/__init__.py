"""
pycclone.formatters
---------------------
"""
import os
from imp import load_source
from importlib import import_module
from pycclone import USERDIR

# Make BaseFormatter available at module level
from pycclone.formatters.base_formatter import BaseFormatter


# === get_formatter(name) ===
def get_formatter(name):
    """
    Loads a formatter module with the given name.
    """

    # Is it already in the path?
    try:
        return import_module('pycclone.formatters.' + name)
    except ImportError:
        pass

    # Import from user folder
    fpath = os.path.join(USERDIR, 'formatters', name, name + '.py')
    return load_source('pycclone.formatters.' + name, fpath)
