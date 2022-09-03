#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(name='HornMorphoO',
      version='4.5',
      description='Morphological analyzer/generator for Afaan Oromoo',
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
                    ['languages/orm/*',
                     'languages/orm/fst/*',
                     'languages/orm/lex/*',
                     'languages/orm/cas/*',
                     'languages/orm/data/*',
#                     'languages/orm/cache/*',
                     'languages/orm/pkl/*.pkl',
                     'docs/horn3_quick.pdf',
                     'morpho/geez/*']
                     },
      exclude_package_data={'hm':
                             ['languages/eng/*',
                              'languages/gru/*',
                              'languages/sgw/*',
                              'languages/a/*',
                              'languages/ior/*',
                              'languages/muh/*',
                              'languages/mvx/*',
                              'languages/wle/*',
                              'languages/amh/*',
                              'languages/som/*',
                              'languages/stv/*',
                              'languages/tir/*',
                              'languages/tig/*']
                              }
                             )
