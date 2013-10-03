"""
pycclone
--------

A simple extensible documentation generator
"""
import json
from glob import glob
import os
import pkg_resources

# === Module Constants ===
# Define documentation settings by adding a `pycclone.json` file to your project
# directory.
# ```
# {
#     "main": {
#         "template": "template name",
#         "formatter": "formatter name",
#         "highlighter": "highlighter name",
#     },
#     "template": {
#         "option": "value",
#         "anotheroption": true
#         ...
#     },
#     "formatter": {
#         ...
#     },
#     "highlighter": {
#         ...
#     }
# }
# ```
# The `main` section is used to load the appropriate modules, and command line
# arguments can be specified here.
# The other sections are passed to their classes as `**kwargs`
SETTINGSFILE = 'pycclone.json'


# This is where plugins can be extracted to for pycclone to recognize them.
# Templates, languages, formatters, and highlighters should go in subdirectories
# of this folder.
if 'XDG_CONFIG_HOME' in os.environ:
    USERDIR = os.path.join(os.environ['XDG_CONFIG_HOME'], '.pycclone')
elif 'APPDATA' in os.environ:
    USERDIR = os.path.join(os.environ['APPDATA'], '.pycclone')
else:
    USERDIR = os.path.join(os.environ['HOME'], '.pycclone')

# === Language Definitions ===
# Languages are stored in json files under `USERDIR/languages` with
# the following format:
# `languages/python.json`
# ```
# { ".py": {
#     "name": "python",
#     "symbol": "#",
#     "multistart": "\"\"\"",
#     "multiend": "\"\"\"",
#     }
# }
# There is currently no support for multiple multi-line delimiters.
# For example, using `'''` for multiline comments instead of `"""`
# in python is not supported.
# ```
LANG = {}

# Read packaged languages
for lang in pkg_resources.resource_listdir('pycclone', 'data/languages'):
    fname = 'data/languages/' + lang
    stream = pkg_resources.resource_stream('pycclone', fname)
    LANG.update(json.loads(stream.read()))

# Read locally installed languages
for lang in glob(os.path.join(USERDIR, 'languages', '*.json')):
    with open(lang, 'r') as f:
        LANG.update(json.loads(f.read()))
