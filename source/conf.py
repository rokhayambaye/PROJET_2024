# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ANALYSE DU TRAFIC CYCLISTE'
copyright = "2024, DIALLO Ousmane , M'RAD Samy , MBAYE Rokhaya, ROMANI DE VINCI Coralie"
author = "DIALLO Ousmane , M'RAD Samy , MBAYE Rokhaya, ROMANI DE VINCI Coralie"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",      # Documentation automatique des docstrings
    "sphinx.ext.napoleon",     # Support des formats de docstrings Google et NumPy
    "sphinx_rtd_theme",        # Thème Read the Docs
    ]

templates_path = ['_templates']
exclude_patterns = []
language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
import os
import sys
sys.path.insert(0, os.path.abspath('../bike/Base_des_donnees/'))
sys.path.insert(0, os.path.abspath('../bike'))
sys.path.insert(0, os.path.abspath('../installer'))
sys.path.insert(0, os.path.abspath('../traitement_donnee'))