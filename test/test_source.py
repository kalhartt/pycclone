"""
test/test_source.py

Test pycclone.source module
"""
import os
from nose.tools import raises
from pycclone.source import Source, ParseError
from pycclone.formatters import BaseFormatter
from pycclone.highlighters import BaseHighlighter
from pycclone.templates import BaseTemplate

_basepath = os.path.join('test', 'test_samples')


def test_detect_language():
    src = Source(os.path.join(_basepath, 'single_line_comment.py'))
    src.detect_language()
    assert src.lang['name'] == 'python'


def test_singleline():
    path = os.path.join(_basepath, 'single_line_comment.py')
    src = Source(path)
    sections = list(src.read_sections())
    assert len(sections) == 2
    assert sections[1][0] == ' This is a single line comment\n'


def test_singleline_hidden():
    path = os.path.join(_basepath, 'single_line_comment_hidden.py')
    src = Source(path)
    sections = list(src.read_sections())
    assert len(sections) == 1
    assert sections[0][0] == ''


def test_multiline():
    path = os.path.join(_basepath, 'multi_line_comment.py')
    src = Source(path)
    sections = list(src.read_sections())
    assert len(sections) == 1
    assert sections[0][0] == ''.join([
        '\n',
        'This is a multiline comment.\n',
        'The total line comment length is 4 lines.\n',
        '\n'])


def test_multiline_hidden():
    path = os.path.join(_basepath, 'multi_line_comment_hidden.py')
    src = Source(path)
    sections = list(src.read_sections())
    assert len(sections) == 1
    assert sections[0][0] == ''


@raises(ParseError)
def test_multiline_unmatched():
    path = os.path.join(_basepath, 'multi_line_unmatched.py')
    src = Source(path)
    sections = list(src.read_sections())
    return sections


def test_generate_docs_file():
    path = os.path.join(_basepath, 'single_line_comment.py')
    src = Source(path)
    src.generate_docs(
        BaseTemplate(),
        BaseFormatter(),
        BaseHighlighter(),
        os.path.join('test', 'test_out'))
    outpath = os.path.join(
        'test',
        'test_out',
        _basepath,
        'single_line_comment')
    outfile = [
        'def this_is_some_code():\n',
        ' This is a single line comment\n',
        '    pass\n']

    with open(outpath, 'r') as f:
        lines = f.readlines()

    for outline, writtenline in zip(outfile, lines):
        assert outline == writtenline, '%r %r' % (outline, writtenline)


def test_generate_docs_string():
    path = os.path.join(_basepath, 'single_line_comment.py')
    src = Source(path)
    result = src.generate_docs(
        BaseTemplate(),
        BaseFormatter(),
        BaseHighlighter(),
        None)
    outfile = ''.join([
        'def this_is_some_code():\n',
        ' This is a single line comment\n',
        '    pass\n'])
    assert result == outfile
