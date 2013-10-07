"""
pycclone.highlighters
---------------------
"""
import os
from imp import load_source
from importlib import import_module
from pycclone import USERDIR

# Make BaseHighlighter available at module level
from pycclone.highlighters.base_highlighter import BaseHighlighter


# === get_highlighter(name) ===
def get_highlighter(name):
    """
    Loads a highlighter module with the given name.
    """

    # Is it already in the path?
    try:
        return import_module('.' + name, 'pycclone.highlighters')
    except ImportError:
        pass

    # Import from user folder
    fpath = os.path.join(USERDIR, 'highlighters', name, name + '.py')
    return load_source('pycclone.highlighters.' + name, fpath)
