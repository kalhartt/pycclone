"""
pycclone.utils
--------------

Utility functions
"""
import os
import sys

ROOT = os.curdir


def destination(fname, outdir):
    """
    Calculates the destination file (excluding the extension) for a given
    source file.
    """
    if not outdir:
        return fname

    basename, filename = os.path.split(os.path.relpath(fname, ROOT))
    filename, ext = os.path.splitext(filename)
    outname = os.path.relpath(os.path.join(outdir, basename))
    return os.path.join(outname, filename)


def split_path(path):
    """
    Splits a path into a list of its directories and filename
    """
    split = list(os.path.split(path))
    while split[0]:
        split = list(os.path.split(split[0])) + split[1:]
    return split[1:]


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


def copy_static(plugin, fname, outdir):
    """
    Copies file `fname` from plugin directory to output directory root.

    This assumes fname points to a file, not a directory. Relative directory
    structure is preserved.

    ### arguments
    plugin
    :   Reference to the plugin whose static files are being copied. In
        practice this is usually `self`.

    fname
    :   Name of the file to copy

    outdir
    :   Output directory path

    ### returns
    `None`
    """
    ext = os.path.splitext(fname)[1]
    out_name = destination(fname, outdir) + ext
    with open_static(plugin, fname) as f_in:
        with open(out_name, 'w') as f_out:
            f_out.writelines(line for line in f_in)
