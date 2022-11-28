#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(name='HornMorphoAX',
      version='4.5.1',
      description='Morphological segmenter/analyzer for Amharic',
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
      install_requires=["conllu"],
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
                     'languages/amh/pkl/*X*.pkl',
#                     'docs/horn3_quick.pdf',
                     'figs/*',
                     'morpho/geez/*']
                     },
      exclude_package_data={'hm':
                             ['morpho/stv_lang.py',
                              'morpho/ti_lang.py',
                              'morpho/om_lang.py',
                              'morpho/am_lang.py',
                              'proc.py',
                              'test.py',
                              'internet_search.py',
                              'languages/eng/*',
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
