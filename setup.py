from setuptools import setup
import sys

install_requires = ['markdown', 'pygments']
if sys.version_info < (2, 7):
    install_requires = ['importlib', 'argparse']

setup(
    name="pycclone",
    version="0.1.0",
    description="""An extensible rewrite of Pycco, the
    python port of Docco: the original quick-and-dirty hundred-line-long,
    literate-programming-style documentation generator.
    """,
    author="Kalhartt",
    author_email="kalhartt@gmail.com",
    url="http://kalhartt.github.com/pycclone",
    packages=["pycclone", "pycclone.templates", "pycclone.formatters", "pycclone.highlighters"],
    packages_dir={
        "pycclone": "pycclone",
        "pycclone.templates": "pycclone/templates",
        "pycclone.formatters": "pycclone/formatters",
        "pycclone.highlighters": "pycclone/highlighters"
    },
    packages_data={
        "pycclone": "data/*",
        "pycclone.templates": "data/*"
    },
    install_requires=install_requires,
    extras_requires={},
    entry_points={
        "console_scripts": [
            "pycclone = pycclone.main:main",
        ]
    }
)
