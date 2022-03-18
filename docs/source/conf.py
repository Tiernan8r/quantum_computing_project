# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))


# -- Project information -----------------------------------------------------

project = 'Quantum Computing Project'
copyright = '2022, Tiernan8r'
author = 'Tiernan8r, hyoong, JabethM, nys1998, s1960329, RiddhiYaddav'

# The full version, including alpha/beta/rc tags
release = '0.0.3'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.githubpages",
    "sphinx.ext.autodoc",
    "m2r2",
]

m2r_parse_relative_links = True
m2r_anonymous_references = True
autodoc_type_aliases = {
    "SCALARS": "qcp.matrices.types.SCALARS",
    "SCALARS_T": "qcp.matrices.types.SCALARS_T",
    "VECTOR": "qcp.matrices.types.VECTOR",
    "MATRIX": "qcp.matrices.types.MATRIX",
    "SPARSE": "qcp.matrices.types.SPARSE",
}

special_members = ["__init__", "__add__", "__sub__", "__mul__",
                   "__rmul__", "__len__", "__setitem__", "__getitem__",
                   "__str__"]
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": True,
    "special-members": ",".join(special_members),
    "exlude-members": "_abc_impl"
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
