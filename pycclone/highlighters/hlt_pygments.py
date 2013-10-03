"""
pycclone.highlighters.pygments
------------------------------

pygment based code highlighther
"""
import os
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

class Highlighter(object):

    def __init__(self, **kwargs):
        self.args = kwargs
        self.formatter = HtmlFormatter(**self.args['formatter'])

    def copy_static(self, outdir):
        """
        Copies static files to the output directory

        This is not called if outputting to stdout
        """
        with open(os.path.join(outdir, 'pygments.css'), 'w') as f:
            f.write(self.formatter.get_style_defs('.pygments'))

    def highlight(self, code, language):
        """
        Highlights a single chunk of code using the **Pygments** module.

        kwargs is the dictionary `highlight_args` defined in `pycclone.json`
        settings.
        """
        lexer = get_lexer_by_name(language['name'], **self.args['lexer'])
        return pygments.highlight(code, lexer, self.formatter)
