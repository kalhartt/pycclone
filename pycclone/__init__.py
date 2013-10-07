"""
pycclone
--------

A simple extensible documentation generator

### Module Constants
"""
import os

#This is the file we look for to load settings from.
#All the options are listed in [pycclone.main](/pycclone/docs/main.html#settings).
#You can view the settings file used to generate these pages [here](https://github.com/kalhartt/pycclone/blob/master/pycclone.json).
SETTINGSFILE = 'pycclone.json'


#This is where plugins can be extracted to for pycclone to recognize them.
#Templates, languages, formatters, and highlighters should go in subdirectories
#of this folder. To see how plugins are loaded from these directories, check
#the `__init__.py` of the plugin module.
if 'XDG_CONFIG_HOME' in os.environ:
    USERDIR = os.path.join(os.environ['XDG_CONFIG_HOME'], '.pycclone')
elif 'APPDATA' in os.environ:
    USERDIR = os.path.join(os.environ['APPDATA'], '.pycclone')
else:
    USERDIR = os.path.join(os.environ['HOME'], '.pycclone')
