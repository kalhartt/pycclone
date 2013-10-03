"""
pycclone.formatters.markdown
----------------------------

Markdown document formatting
"""
from markdown import markdown

class Formatter(object):

    def __init__(self, **kwargs):
        self.args = kwargs

    def format(self, docs, language):
        """
        Formats a document section using markdown.

        kwargs is the dictionary `format_args` defined in `pycclone.json`
        settings.
        """
        return markdown(docs, **self.args)
