import os
import sys
sys.path.insert(0, os.path.abspath('.'))

# Add any Sphinx extension module names here, as strings.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
