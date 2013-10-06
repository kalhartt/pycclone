"""
test/test_languages.py

Ensure that language definitions are appropriately
loaded and parsed from both package data and local
installation in pycclone.USERDIR
"""
import imp
from pycclone import languages
from mock import patch

_keys = ['name', 'extension', 'symbol', 'multistart', 'multiend']
pkg_langs = [
    'c',
    'coffee-script',
    'cpp',
    'erlang',
    'haskell',
    'javascript',
    'lua',
    'perl',
    'python',
    'ruby',
    'scheme',
    'sql',
    'tcl'
]
pkg_exts = [
    '.c',
    '.coffee',
    '.cpp',
    '.erl',
    '.hs',
    '.js',
    '.lua',
    '.pl',
    '.py',
    '.rb',
    '.scm',
    '.sql',
    '.tcl'
]


@patch('pycclone.USERDIR', 'DNE')
def test_lang_from_pkg():
    """Test languages included with this package."""
    imp.reload(languages)
    for lang in pkg_langs:
        assert lang in languages._LANG, 'Language not loaded %s' % lang
        for key in _keys:
            assert key in languages._LANG[lang], 'Language %s missing %s' % (lang, key)


@patch('pycclone.USERDIR', './test/userdir')
def test_lang_from_local():
    """Test languages installed to USERDIR."""
    imp.reload(languages)
    assert 'test_language' in languages._LANG, 'Failed to load test language from USERDIR'
    for key in _keys:
        assert key in languages._LANG['test_language'], 'Language test missing %s' % key


def test_lang_by_name():
    """Test languages installed to USERDIR."""
    for name in pkg_langs:
        lang = languages.get_by_name(name)
        for key in _keys:
            assert key in lang, 'Language %s missing %s' % (name, key)


def test_lang_by_ext():
    """Test languages installed to USERDIR."""
    for ext in pkg_exts:
        lang = languages.get_by_ext(ext)
        for key in _keys:
            assert key in lang, 'Language %s missing %s' % (ext, key)
