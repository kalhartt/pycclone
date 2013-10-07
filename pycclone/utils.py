"""
pycclone.utils
--------------

Utility functions
"""
import os
import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

DESTROOT = ''


def destination(fname, outdir):
    """
    Calculates the destination file (excluding the extension) for a given
    source file.
    """
    if not outdir:
        return fname

    filename = os.path.splitext(os.path.relpath(fname, DESTROOT))[0]
    return os.path.join(outdir, filename)


def split_path(path):
    """
    Splits a path into a list of its directories and filename
    """
    split = list(os.path.split(path))
    while split[0]:
        split = list(os.path.split(split[0])) + split[1:]
    return split[1:]


class file_or_stdout(object):
    """
    Context manager returning either a file handle
    or a StringIO instance.
    """

    def __init__(self, fname, outdir, ext):
        self.fname = fname
        self.outdir = outdir
        self.ext = ext

    def __enter__(self):
        if not self.outdir:
            self.fhandle = StringIO()
        else:
            outname = destination(self.fname, self.outdir) + self.ext
            outdir = os.path.dirname(outname)
            if not os.path.isdir(outdir):
                os.makedirs(outdir)
            self.fhandle = open(outname, 'w')
        return self.fhandle

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.outdir:
            sys.stdout.write(self.fname + '\n')
            sys.stdout.write(self.fhandle.getvalue())
            sys.stdout.write('\n')
            sys.stdout.flush()
        self.fhandle.close()


class open_static(object):
    """
    Context Manager for handling a plugin's static assets.

    A convenience class for opening static assets in the same folder as
    the template module. If you are packaging your template, ignore
    this method and use pkg_resources.
    """

    def __init__(self, plugin, fname):
        """
        Setup the context manager
        """
        path = os.path.dirname(sys.modules[plugin.__module__].__file__)
        self.fname = os.path.join(path, fname)

    def __enter__(self):
        self.fhandle = open(self.fname, 'rU')
        return self.fhandle

    def __exit__(self, exc_type, exc_value, traceback):
        self.fhandle.close()
