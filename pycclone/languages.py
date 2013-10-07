"""
# pycclone.languages

Languages are stored in json files under `USERDIR/languages` with
the following format:

`languages/<name>.json`
```
{ "<name>": {
    "name": "<name>",
    "extension": "<extension>",
    "symbol": "<single-line identifier>",
    "multistart": "<multi-line begin identifier>",
    "multiend": "<multi-line end identifier>"
    }
}
```
"""
import json
import os
import pkg_resources as pkg
from glob import glob
from pycclone import USERDIR

_LANG = {}

# Read packaged languages
for lang in pkg.resource_listdir('pycclone', 'data/languages'):
    fname = 'data/languages/' + lang
    stream = pkg.resource_stream('pycclone', fname)
    _LANG.update(json.loads(stream.read().decode('utf-8')))

# Read locally installed languages
for lang in glob(os.path.join(USERDIR, 'languages', '*.json')):
    with open(lang, 'rU') as f:
        _LANG.update(json.loads(f.read()))


def get_by_name(name):
    """Returns the language with a given name."""
    if name in _LANG:
        return _LANG[name]
    raise ValueError("Cannot determine language for %s" % name)


def get_by_ext(ext):
    """Returns the language with a given extension."""
    for k, v in _LANG.items():
        if v['extension'] == ext:
            return v
    raise ValueError("Cannot determine language for %s" % ext)
