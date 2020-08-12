#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(name='HornMorphoAK',
      version='4.0',
      description='Morphological analyzer/generator for Amharic and Kistane',
      author='Michael Gasser',
      author_email='gasser@indiana.edu',
      url='http://homes.soic.indiana.edu/gasser/plogs.html',
      license="GPL v3",
      packages=find_packages("hm"),
      package_dir={'': "hm"},
      package_data={'languages':
                    ['amh/*',
                     'amh/fst/*',
                     'amh/lex/*',
                     'amh/cas/*',
                     'amh/data/*',
                     'amh/cache/*',
                     'gru/*',
                     'gru/fst/*',
                     'gru/lex/*',
                     'gru/cas/*',
                     'gru/cache/*'],
                     '': ['*.txt'],
                     'docs': ['horn3_quick.pdf']
                     }
#      exclude_package_data= {'hm':
#                             ['languages/am/*',
#                              'languages/en/*',
#                              'languages/sgw/*',
#                              'languages/om/*',
#                              'languages/som/*',
#                              'languages/stv/*'
#                              'languages/ti/*',
#                              'languages/tig/fst/*']
#                              }
                             )
