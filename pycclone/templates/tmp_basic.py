"""
pycclone.templates.basic
------------------------

This is as simple as it gets folks.
"""
from pycclone.templates import BaseTemplate

class Template(BaseTemplate):
    """
    An extremely basic template.
    """
    ext = '.html'

    def generate_docs(self, sections):
        yield '<html><body>\n'
        for docs, code in sections:
            yield docs + code
        yield '</html></body>'
