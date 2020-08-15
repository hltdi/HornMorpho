#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(name='HornMorphoA',
      version='4.0',
      description='Morphological analyzer/generator for Amharic and Kistane',
      author='Michael Gasser',
      author_email='gasser@indiana.edu',
      url='http://homes.soic.indiana.edu/gasser/plogs.html',
      license="GPL v3",
      install_requires=["yaml>=5.0"],
      packages=find_packages("src"),
      package_dir={'': "src"},
      package_data={'hm':
                    ['languages/amh/*',
                     'languages/amh/fst/*',
                     'languages/amh/lex/*',
                     'languages/amh/cas/*',
                     'languages/amh/data/*',
                     'languages/amh/cache/*',
                     'languages/gru/*',
                     'languages/gru/fst/*',
                     'languages/gru/lex/*',
                     'languages/gru/cas/*',
                     'languages/gru/cache/*',
                     'docs/horn3_quick.pdf',
                     'morpho/geez/*']
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
