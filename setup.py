#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='HornMorpho',
      version='4.0.2',
      description='Morphological analyzer/generator for languages of the Horn of Africa',
      author='Michael Gasser',
      author_email='gasser@indiana.edu',
      url='http://homes.soic.indiana.edu/gasser/plogs.html',
      license="GPL v3",
#      install_requires=["yaml>=5.0"],
      packages=find_packages("src"),
      package_dir={'': "src"},
      package_data = {'hm':
                      ['languages/amh/*',      'languages/amh/cas/*',
                       'languages/amh/fst/*',  'languages/amh/lex/*',
                       'languages/amh/stat/*', 'languages/amh/data/*',
                       'languages/gru/*',      'languages/gru/cas/*',
                       'languages/gru/fst/*',  'languages/gru/lex/*',
                       'languages/tir/*',      'languages/tir/cas/*',
                       'languages/tir/fst/*',  'languages/tir/lex/*',
                       'languages/tir/stat/*', 'languages/tir/data/*',
                       'languages/tig/*',      'languages/tig/cas/*',
                       'languages/tig/fst/*',  'languages/tig/lex/*',
                       'languages/sgw/*',      'languages/sgw/cas/*',
                       'languages/sgw/fst/*',  'languages/sgw/lex/*',
                       'languages/som/*',      'languages/som/cas/*',
                       'languages/som/fst/*',  'languages/som/lex/*',
                       'languages/orm/*',      'languages/orm/cas/*',
                       'languages/orm/fst/*',  'languages/orm/lex/*',
                       'languages/orm/stat/*', 'languages/orm/data/*',
                       'docs/horn3_quick.pdf',
                       'morpho/geez/*']}
     )
