#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Meerkat documentation build configuration file, created by
# sphinx-quickstart on Wed Feb 14 16:59:58 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import pip
import shutil
import importlib
import os
from shutil import copyfile
import sys
import logging
from collections import OrderedDict
from unittest.mock import MagicMock
sys.path.insert(0, os.path.abspath('.'))

 
# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

from recommonmark.parser import CommonMarkParser

source_parsers = {
    '.md': CommonMarkParser,
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Meerkat'
copyright = '2018, Meerkat Developers'
author = 'Meerkat Developers'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = ''
# The full version, including alpha/beta/rc tags.
release = ''

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'classic'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'Meerkatdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Meerkat.tex', 'Meerkat Documentation',
     'Jonathan Berry', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'meerkat', 'Meerkat Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'Meerkat', 'Meerkat Documentation',
     author, 'Meerkat', 'One line description of project.',
     'Miscellaneous'),
]


# -- Combine Meerkat's documentation --------------------------------------

# Meerkat's docs are spread across a variety of different repos.
# Here we assume that all DOCUMENTED_REPOS exist in the file system under
# the REPO_DIRECTORY and they include a sub folder "docs" with a "source"
# folder containing the file "conf.py". The code below installs all relavent
# dependancies copies across the docs source and amalgamates the configs
# so that we can render a single set of master documentation.

DOCUMENTED_REPOS = [
    'meerkat_auth',
    'meerkat_hermes',
    'meerkat_api',
    'meerkat_abacus',
    'meerkat_libs',
    'meerkat_frontend',
    'meerkat_infrastructure',
    'meerkat_nest',
    'meerkat_dev',
    'meerkat_analysis',
    'meerkat_country_server',
    'meerkat_drill'
    
]
REPO_DIRECTORY = "/var/www/"
SERVICES_DIRECTORY = "services/"


def install_packages():
    for package in DOCUMENTED_REPOS:

        logging.info("\n-- Now installing {} --\n".format(package))
        sys.path.insert(0, REPO_DIRECTORY + package)
        requirements_file_path = REPO_DIRECTORY + package + "/requirements.txt"
        if os.path.exists(REPO_DIRECTORY + package + "/docs/requirements.txt"):
            requirements_file_path = REPO_DIRECTORY + package + "/docs/requirements.txt"

        copyfile(requirements_file_path, "req.txt")
        with open("new-req.txt", "w") as f:
            with open("req.txt") as f2:
                for line in f2:
                    if "python-dateutil" in line:
                        f.write("python-dateutil==2.6\n")
                    else:
                        f.write(line.split("==")[0] + "\n")
        pip.main(['install', '-r', "new-req.txt"])
        pip.main(['install', '--no-deps', '-e', REPO_DIRECTORY + package])


def assemble_source():
    for package in DOCUMENTED_REPOS:
        try:
            shutil.rmtree(SERVICES_DIRECTORY + package, ignore_errors=True)
            shutil.copytree(
                REPO_DIRECTORY + package + '/docs/source',
                SERVICES_DIRECTORY + package
            )
        except FileNotFoundError:
            logging.warning("No docs available for {}".format(package))


def setup_extensions():
    extensions = []
    services_package = SERVICES_DIRECTORY[:-1] + "."
    for package in DOCUMENTED_REPOS:
        try:
            conf = importlib.import_module(services_package+package+'.conf')
            extensions += conf.extensions
        except ImportError:
            logging.warning("No docs configuration for {}".format(package))
    return list(OrderedDict.fromkeys(extensions))


def setup_autodoc_mocks():
    autodoc_mock_imports = set([])
    services_package = SERVICES_DIRECTORY[:-1] + "."
    for package in DOCUMENTED_REPOS:
        try:
            conf = importlib.import_module(services_package+package+'.conf')
            autodoc_mock_imports.update(conf.autodoc_mock_imports)
        except ImportError:
            logging.warning("No docs configuration for {}".format(package))
        except AttributeError:
            logging.warning("No mocks for {}".format(package))
    return list(autodoc_mock_imports)

    
def remove_package(to_remove, mocks):
    final = []
    for m in mocks:
        found = False
        for remove in to_remove:
            if remove in m:
                found = True
                break
        if not found:
            final.append(m)
    return final


install_packages()
assemble_source()

autodoc_mock_imports = remove_package(DOCUMENTED_REPOS, setup_autodoc_mocks())
# mock_modules(manual_mocks)
print(autodoc_mock_imports)

extensions += setup_extensions()
