#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(name='HornMorpho',
      version='4.1',
      description='Morphological analyzer/generator for languages of the Horn of Africa',
      author='Michael Gasser',
      author_email='gasser@indiana.edu',
      url='http://homes.soic.indiana.edu/gasser/plogs.html',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3',
          'Topic :: Text Processing'
      ],
#      install_requires=["yaml>=5.0"],
      python_requires='>=3',
      packages=find_packages("src"),
      package_dir={'': "src"},
      package_data = {'hm':
                      ['languages/amh/*',      'languages/amh/cas/*',
                       'languages/amh/fst/*',  'languages/amh/lex/*',
                       'languages/amh/stat/*', 'languages/amh/data/*',
                       'languages/amh/pkl/*.pkl',
#                       'languages/gru/*',      'languages/gru/cas/*',
#                       'languages/gru/fst/*',  'languages/gru/lex/*',
#                       'languages/gru/pkl/*.pkl',
                       'languages/tir/*',      'languages/tir/cas/*',
                       'languages/tir/fst/*',  'languages/tir/lex/*',
                       'languages/tir/stat/*', 'languages/tir/data/*',
                       'languages/tir/pkl/*.pkl',
#                       'languages/tig/*',      'languages/tig/cas/*',
#                       'languages/tig/fst/*',  'languages/tig/lex/*',
#                       'languages/tig/pkl/*.pkl',
#                       'languages/sgw/*',      'languages/sgw/cas/*',
#                       'languages/sgw/fst/*',  'languages/sgw/lex/*',
#                       'languages/sgw/pkl/*.pkl',
                       'languages/som/*',      'languages/som/cas/*',
                       'languages/som/fst/*',  'languages/som/lex/*',
                       'languages/som/pkl/*.pkl',
                       'languages/orm/*',      'languages/orm/cas/*',
                       'languages/orm/fst/*',  'languages/orm/lex/*',
                       'languages/orm/stat/*', 'languages/orm/data/*',
                       'languages/orm/pkl/*.pkl',
                       'docs/horn3_quick.pdf',
                       'morpho/geez/*']}
     )
