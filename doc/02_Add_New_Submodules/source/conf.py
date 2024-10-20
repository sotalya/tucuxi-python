

# -*- coding: utf-8 -*-
#
# user manual documentation build configuration file, created by
# sphinx-quickstart on Tue Dec  8 11:23:11 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os

template_path = 'C:/Users/admin/Documents/Tucuxi/tucuxi-doc/01_General/00_Templates'
exec(open(template_path + '/general_conf.py').read())


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'


# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'how_to_add_modules'


# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '1.0'
# The full version, including alpha/beta/rc tags.
release = '1.0'


# Output file base name for HTML help builder.
htmlhelp_basename = 'how_to_add_modules'


# -- Options for LaTeX output ---------------------------------------------


# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  ('how_to_add_modules', 'how_to_add_modules.tex', u'How to add a Module',
   u'Tucuxi dev team', 'manual'),
]



