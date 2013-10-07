"""
pycclone.templates
------------------

Module containing all pycclone templates.
"""
import os
from imp import load_source
from importlib import import_module
from pycclone import USERDIR

# Make the base template available at module level
from pycclone.templates.base_template import BaseTemplate

# === get_template(name) ===
def get_template(name):
    """
    Loads a template module with the given name.
    **Template classes are not validated.**
    """

    # Is it already in the path?
    try:
        return import_module('pycclone.templates.' + name)
    except ImportError:
        pass

    # Import from user folder
    fpath = os.path.join(USERDIR, 'templates', name, name + '.py')
    return load_source('pycclone.templates.' + name, fpath)
