#!/usr/bin/env python3
### NOTE: THIS CURRENTLY FAILS TO EXCLUDE OTHER LANGUAGES!
from setuptools import setup, find_packages

setup(name='HornMorphoT',
      version='4.0.4',
      description='Morphological analyzer/generator for Tigrinya and Tigre',
      author='Michael Gasser',
      author_email='gasser@indiana.edu',
      url='http://homes.soic.indiana.edu/gasser/plogs.html',
      license="GPL v3",
#      install_requires=["yaml>=5.0"],
      packages=find_packages("src"),
      package_dir={'': "src"},
      package_data={'hm':
                    ['languages/tir/*',
                     'languages/tir/fst/*',
                     'languages/tir/lex/*',
                     'languages/tir/cas/*',
                     'languages/tir/data/*',
                     'languages/tir/cache/*',
                     'languages/tig/*',
                     'languages/tig/fst/*',
                     'languages/tig/lex/*',
                     'languages/tig/cas/*',
                     'languages/tig/cache/*',
                     'docs/horn3_quick.pdf',
                     'morpho/geez/*']
                     },
      exclude_package_data={'hm':
                             ['languages/eng/*',
                              'languages/sgw/*',
                              'languages/om/*',
                              'languages/som/*',
                              'languages/stv/*'
                              'languages/amh/*',
                              'languages/gru/*']
                              }
                             )
