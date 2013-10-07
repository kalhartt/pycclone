"""
pycclone.highlighters.base_highlighter
------------------------------

Base Highlighter class
"""


class BaseHighlighter(object):

    def __init__(self, **kwargs):
        """
        Setup the highlighter

        kwargs is the dictionary defined as `highlighter_args`
        in the `pycclone.json` settings. It defaults to an empty
        dict.
        """
        pass

    def copy_static(self, outdir):
        """
        Copies static files to the output directory

        This is not called if outputting to stdout
        """
        pass

    def highlight(self, code, language):
        """
        Highlights a single chunk of code with the given language.

        argsuments
        code - string read from the code file
        language - language dictionary defined in json files

        returns
        string - modified code
        """
        return code
