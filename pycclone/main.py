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

    # Supported command line arguments are
    # Short | Long | Parameters | Description
    # -p | --paths | |If given, output documentation structure will mirror the source code structure
    # -d | --directory | str | If given, output documentation will be written into this folder. Otherwise it is printed to stdout
    # -i | --index-file | str | Filenames matching this pattern will be written out as index.html instead of filename.html
    # -l | --language | str | Forces the language to a given language. Languages are added here #TODO
    # src | | str[] | List of files to have documentation generated
    parser = argparse.ArgumentParser(description='Generate documentation from sourcecode')
    parser.add_argument('-p', '--paths', action='store_true', default=None,
                        help='Preserve path structure of original files')
    parser.add_argument('-d', '--directory', action='store', type=str, default=None,
                        help='Output directory, writes to stdout if unspecified')
    parser.add_argument('-i', '--index-file', action='store', type=str, default=None,
                        help='Filename pattern to generate index.html from')
    parser.add_argument('-l', '--language', action='store', type=str, default=None,
                        help='Force the language for the given files')
    parser.add_argument('src', action='store', type=str, nargs='+', default=None,
                        help='Files to generate documentation for')

    # Filter out arguments that weren't actually passed on the commandline
    args = dict((k, v) for k, v in vars(parser.parse_args()).items() if v is not None)
    logging.debug('Parsed args: %s', args)

    # Since the commandline arguments were filtered, we can't use defaults
    # provided by argparse. Instead use a default value dictionary
    # `None` is a special value for directory that forces output to STDOUT
    settings = {
        'directory': None,
        'template': 'basic',
        'formatter': 'markdown',
        'highlighter': 'pygments',
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

    template.preprocess([utils.destination(x, settings['directory']) for x in settings['src']])
    for src in settings['src']:
        Source(src).generate_docs(template, formatter, highlighter, settings['directory'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
