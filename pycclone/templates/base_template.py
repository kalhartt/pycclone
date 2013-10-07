"""
pycclone.templates.base_template
--------------------------------
"""


# === Base Template ===
class BaseTemplate(object):
    """Parent class for all pycclone templates"""

    # The output file extension
    ext = ''

    def __init__(self, **kwargs):
        """
        Setup the template object.

        The first argument is a list of target output filenames including paths
        relative to the output directory. The keyword arguments are from the
        dictionary provided as `template_args` in `pycclone.json`.
        Common tasks:
        * Parse settings
        * Cache assets
        * Generate navigation links
        """
        pass

    def copy_static(self, outdir):
        """
        Copies static files to output folder.

        copy_static will not be called if writing to stdout.
        """
        pass

    # === Output Generating Methods ===

    def preprocess(self, sources, root_link):
        """
        Setup the template for the project with the given sources.

        Called with a list of files to generate documentation for before
        any of them have been processed. This can be used to generate headers
        and navigation. If multiple projects are being processed, preprocess
        will be called before beginning each project.
        """
        pass

    def generate_docs(self, sections):
        """
        Generates the document.

        The argument sections is a generator yielding `(docs, code)` tuples.
        This **must** be a generator yielding strings to write to the out.
        If you insist on manipulating the whole file in memory, then just
        use yield instead of return at the end.
        """
        pass
