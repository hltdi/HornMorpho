#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(name='HornMorphoA',
      version='4.3',
      description='Morphological analyzer/generator for Amharic',
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
      package_data={'hm':
                    ['languages/amh/*',
                     'languages/amh/fst/*',
                     'languages/amh/lex/*',
                     'languages/amh/cas/*',
                     'languages/amh/data/*',
                     'languages/amh/cache/*',
                     'languages/amh/pkl/*.pkl',
                     'docs/horn3_quick.pdf',
                     'morpho/geez/*']
                     },
      exclude_package_data={'hm':
                             ['languages/eng/*',
                              'languages/gru/*'
                              'languages/sgw/*',
                              'languages/a/*',
                              'languages/ior/*'
                              'languages/muh/*'
                              'languages/wle/*'
                              'languages/orm/*',
                              'languages/som/*',
                              'languages/stv/*'
                              'languages/tir/*',
                              'languages/tig/*']
                              }
                             )
