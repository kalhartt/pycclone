"""
pycclone.main
=============

This is where the commandline interface is built.
"""
import argparse
import logging
import json
import pycclone
import os
import sys
from pycclone import utils
from pycclone.templates import get_template
from pycclone.highlighters import get_highlighter
from pycclone.formatters import get_formatter
from .source import Source

log = logging.getLogger(__name__)

# The command-line entry point
def main():
    logging.info('Parsing commandline arguments')
    
    ###Commandline Arguments
    parser = argparse.ArgumentParser(
            description='Generate documentation from sourcecode')
    parser.add_argument(
            '-d',
            '--directory',
            action='store',
            type=str,
            default=None,
            help='Output directory, writes to stdout if unspecified')
    parser.add_argument(
            '-l',
            '--language',
            action='store',
            type=str,
            default=None,
            help='Force the language for the given files')
    parser.add_argument(
            '-r',
            '--root-link',
            action='store',
            type=str,
            default=None,
            help='Path to prepend to all links, must have a trailing "/"')
    parser.add_argument('src',
            action='store',
            type=str,
            nargs='+',
            default=None,
            help='Files to generate documentation for')

    # Filter out arguments that weren't actually passed on the commandline
    args = dict((k, v) for k, v in vars(parser.parse_args()).items() if v is not None)
    logging.debug('Parsed args: %s', args)

    # Since the commandline arguments were filtered, we can't use defaults
    # provided by argparse. Instead use a default value dictionary
    # `None` is a special value for directory that forces output to STDOUT
    settings = {
        'directory': None,
        'root_link': '/',
        'template': 'tmp_basic',
        'formatter': 'fmt_markdown',
        'highlighter': 'hlt_pygments',
        'template_args': {},
        'formatter_args': {},
        'highlighter_args': {
            'lexer': {},
            'formatter': {}
        },
   }

    # Read the local settings file if present and update
    # with the command line arguments
    if os.path.isfile(pycclone.SETTINGSFILE):
        with open(pycclone.SETTINGSFILE, 'r') as f:
            settings.update(json.loads(f.read()))
    settings.update(args)
    logging.debug('Parsed settings: %s', settings)
    
    # Get the modules requested.
    template = get_template(settings['template']).Template(**settings['template_args'])
    formatter = get_formatter(settings['formatter']).Formatter(**settings['formatter_args'])
    highlighter = get_highlighter(settings['highlighter']).Highlighter(**settings['highlighter_args'])

    # Setup the output directory
    if settings['directory']:
        if not os.path.isdir(settings['directory']):
            os.makedirs(settings['directory'])
        template.copy_static(settings['directory'])
        highlighter.copy_static(settings['directory'])

    # Tell utils.destination which dir to treat as output root
    utils.DESTROOT = os.path.dirname(os.path.commonprefix(settings['src']))

    template.preprocess([utils.destination(x, settings['directory']) for x in settings['src']], settings['root_link'])
    for src in settings['src']:
        Source(src).generate_docs(template, formatter, highlighter, settings['directory'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
