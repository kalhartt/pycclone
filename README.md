[![Build Status](https://travis-ci.org/kalhartt/pycclone.png?branch=master)](https://travis-ci.org/kalhartt/pycclone)

pycclone
========

A plugin based documentation generator based off the [Docco](http://jashkenas.github.io/docco/) and [Pycco](http://fitzgen.github.io/pycco/) projects.
Check out the [self-generated documentation](http://kalhartt.github.io/pycclone/docs/main.html)

### Why pycclone?

Docco and its relatives are quite wonderful; however, its monolithic nature makes extension and customization rather painful.
Pycclone aims to be easily extensible and styleable by implementing an extremely simple plugin architecture.

### Features

* Massively extendable plugin architecture while keeping the template classes clean and simple.
* Simple json configuration
* Separates comments intened as documentation and those intended inline with code
  * Documentation comments begin the line
  * Inline comments occer after some code on a line
  * If a multiline comment is started after code, the whole comment block is inlined with the code


### Unfeatures

#### Special handling of files intended as index files or non-code files

Some documentation generators let you write an `index.md` file and will parse it to a special non-code index page.
Pycclone will never support this, it is strictly for generating a static page for each code file.
