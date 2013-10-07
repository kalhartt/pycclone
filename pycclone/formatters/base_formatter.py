"""
pycclone.formatters.base_formatter
----------------------------

Base Formatter class.
"""


class BaseFormatter(object):

    def __init__(self, **kwargs):
        """
        Setup the formatter

        kwargs is the dictionary `format_args` defined in `pycclone.json`
        settings.
        """
        pass

    def format(self, docs, language):
        """
        Formats a document section.
        """
        return docs
