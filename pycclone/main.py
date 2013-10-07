"""
pycclone.main
=============

This is where the commandline interface is built.
"""
import argparse
import logging
import json
import pycclone
import sys
import os
from pycclone import utils
from pycclone.templates import get_template
from pycclone.highlighters import get_highlighter
from pycclone.formatters import get_formatter
from pycclone.source import Source

log = logging.getLogger(__name__)


def main():
    """
    The command-line entry point.

    ###Commandline Arguments
    -d --directory
    :   The directory to write documentation to. If this is a false value,
        documentation will be printed to stdout.

    -l --language
    :   Force files to be interpreted as a given language. The string given
        must match a <name> key from the parsed languages.

    src
    :   List of all source files to generate documentation for.
    """
    logging.info('Parsing commandline arguments')

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
        'src',
        action='store',
        type=str,
        nargs='+',
        default=None,
        help='Files to generate documentation for')

    # Filter out arguments that weren't actually passed on the commandline
    args = parser.parse_args().__dict__.items()
    args = dict((k, v) for k, v in args if v is not None)
    logging.debug('Parsed args: %s', args)

    """
    ###Settings

    directory
    :   Writes documentation to stdout by default

    template
    :   The minimal [tmp_basic](/pycclone/docs/templates/tmp_basic.html)
        template is used by default.

    formatter
    :   The included [markdown formatter](/pycclone/docs/formatters/fmt_markdown.html)
        is used by default.

    highlighter
    :   The included [pygments highlighter](/pycclone/docs/highlighters/hlt_pygments.html)
        is used by default.

    The `<plugin>_args` settings are specific to the plugin used and passed
    **as is** to the plugin's `__init__` method. See that plugin's
    documentation for details.
    """
    settings = {
        'directory': None,
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

    if os.path.isfile(pycclone.SETTINGSFILE):
        with open(pycclone.SETTINGSFILE, 'r') as f:
            settings.update(json.loads(f.read()))
    settings.update(args)
    logging.debug('Parsed settings: %s', settings)

    # Get the modules requested.
    template = get_template(settings['template'])
    template = template.Template(**settings['template_args'])
    formatter = get_formatter(settings['formatter'])
    formatter = formatter.Formatter(**settings['formatter_args'])
    highlighter = get_highlighter(settings['highlighter'])
    highlighter = highlighter.Highlighter(**settings['highlighter_args'])

    # Setup the output directory
    if settings['directory']:
        if not os.path.isdir(settings['directory']):
            os.makedirs(settings['directory'])
        template.copy_static(settings['directory'])
        highlighter.copy_static(settings['directory'])

    # Tell utils.destination which parent dirs to ignore when recreating
    # the directory structure.
    utils.ROOT = os.path.dirname(os.path.commonprefix(settings['src']))
    destination = lambda x: utils.destination(x, settings['directory'])
    outfiles = [destination(x) for x in settings['src']]

    template.preprocess(outfiles)
    for src in settings['src']:
        result = Source(src).generate_docs(
            template,
            formatter,
            highlighter,
            settings['directory'])

        if result:
            sys.stdout.write('\n%s\n' % src)
            sys.stdout.write(result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
