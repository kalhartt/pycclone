"""
#pycclone.source

Provides a class for handling source files. The primary goal is to create a
generator yielding (docs, code) tuples from a source file.
"""
import logging
import re
import os
import pycclone.utils as utils
import pycclone.languages as languages

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

log = logging.getLogger(__name__)


class ParseError(Exception):
    """
    ParseError raises when unexpected things happen while separating the
    source file.
    """
    pass


class Source(object):
    """
    Class for source code file.
    """

    def __init__(self, fname):
        """
        Create Source object.
        """
        log.info('Creating Source object for %s', fname)

        self.fname = fname       # filename including path
        self.detect_language()

    ###Helper Methods

    def detect_language(self, language=None):
        """
        Detects language from extension or argument.
        """
        log.info('Detecting language for %s', self.fname)

        if language:
            self.lang = language

        else:
            ext = os.path.splitext(self.fname)[1]
            self.lang = languages.get_by_ext(ext)

        self.ms = self.lang['multistart']
        self.me = self.lang['multiend']
        self.multi_re = re.compile('%s.*?%s' % (self.me, self.ms))
        log.debug('Detected %s for %s', self.lang['name'], self.fname)

    def read_multiline(self, line, f, indent):
        """
        Reads the file until the end of a multiline section.

        It may return multiple multiline sections as one if a new
        multiline section begins on the same line that one ends.
        """
        log.debug('Beginning multiline search at position %d in %s', f.tell(), self.fname)
        result = ''

        n = line.find(self.ms)
        if n >= 0:
            line = line[n + len(self.ms):]

        while line:
            if line[:indent].isspace() and len(line) > indent:
                line = line[indent:]

            if self.me in self.multi_re.sub('', line):
                result += ''.join(line.rsplit(self.me, 1))
                break

            result += line
            line = f.readline()
        else:
            raise ParseError('Unexpected EOF while parsing %s.' % self.fname)

        return result

    # === Access Methods ===

    def read_sections(self):
        """
        Iterator yielding chunks of documentation and code in a tuple.

        This algorithm will never support Whitespace...
        """
        log.info('Reading sections in %s', self.fname)

        with open(self.fname, 'rU') as f:
            docs = ''
            code = ''
            buff = ''

            # Iterate the file
            indent_re = re.compile(r'\s*')
            in_docs = False
            line = f.readline()
            while line:
                line_strip = line.strip()

                # Add blank lines to the nearest code block
                # Ignore blank lines between docs
                if not line_strip:
                    if not in_docs:
                        code += line
                    else:
                        buff += line
                    line = f.readline()
                    continue

                # Determine if the line is documentation or starts multiline
                # documentation
                line_docs = line_strip.startswith(self.lang['symbol'])
                line_multi = line_strip.startswith(self.ms)

                # If we are starting a new section, yield previous section
                if not in_docs and (line_docs or line_multi) and (docs or code):
                    yield (docs, code)
                    docs = ''
                    code = ''

                if line_multi:
                    # Starting multiline comment
                    in_docs = True
                    indent = len(indent_re.match(line).group())
                    docs += self.read_multiline(line, f, indent)

                elif line_docs:
                    # Starting a single line comment
                    in_docs = True
                    index = line.find(self.lang['symbol']) + len(self.lang['symbol'])
                    docs += line[index:]

                elif self.ms in line_strip:
                    # Multiline docs in code block
                    in_docs = False
                    indent = len(indent_re.match(line).group())
                    code += buff + self.read_multiline(line, f, indent)

                else:
                    # Code block
                    in_docs = False
                    code += buff + line

                # reset loop
                buff = ''
                line = f.readline()

            # Final yield
            yield (docs, code)

    def format_sections(self, formatter, highlighter):
        for docs, code in self.read_sections():
            yield (formatter.format(docs, self.lang), highlighter.highlight(code, self.lang))

    # === Generating Method ===

    def generate_docs(self, template, formatter, highlighter, outdir):
        """
        Generates and writes the documentation for the source file.

        If outdir is false, this will return the generated document.
        Otherwise it returns None.
        """
        log.info('Generating docs for %s', self.fname)

        try:
            if outdir:
                outname = utils.destination(self.fname, outdir) + template.ext
                destdir = os.path.dirname(outname)
                if not os.path.isdir(destdir):
                    os.makedirs(destdir)
                f = open(outname, 'w')
            else:
                f = StringIO()

            for line in template.generate_docs(self.format_sections(formatter, highlighter)):
                f.write(line)

            log.info('Documentation written for %s', self.fname)

            if not outdir:
                result = f.getvalue()
            else:
                result = None

        finally:
            f.close()

        return result
