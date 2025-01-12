import sphinx
import os
import sys

# -- Project information -----------------------------------------------------

project = 'Asset-Importer-Lib'
copyright = '2020-2024, Kim Kulling'
author = 'Kim Kulling'

# The full version, including alpha/beta/rc tags
release = 'March 2022 v5.4.3'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'breathe',
]

breathe_projects = { "AssetImporterLib": "API/" }
breathe_default_project = "AssetImporterLib"

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
