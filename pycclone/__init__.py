"""
pycclone
--------

A simple extensible documentation generator
"""
import os

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
