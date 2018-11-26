#!/usr/bin/env python3

import sys

from distutils.core import setup

setup(name='HornMorpho',
      version='2.6',
      description='Morphological analyzer/generator for Amharic, Oromo, Tigrinya',
      author='Michael Gasser',
      author_email='gasser@indiana.edu',
      url='http://homes.soic.indiana.edu/gasser/plogs.html',
      license="GPL v3",
      packages=['l3', 'l3.morpho', 'l3.morpho.geez'],
      package_data = {'l3': ['languages/am/cas/*.cas',
                             'languages/am/fst/*.fst',
                             'languages/am/lex/*.lex',
                             'languages/am/stat/*.dct',
                             'languages/am/data/ag.txt',
                             'languages/ti/cas/*.cas',
                             'languages/ti/fst/*.fst',
                             'languages/ti/lex/*.lex',
                             'languages/ti/stat/*.dct',
                             'languages/ti/data/ti.txt',
                             'languages/om/cas/*.cas',
                             'languages/om/fst/*.fst',
                             'languages/om/lex/*.lex',
                             'languages/om/stat/*.dct'],
                      'l3.morpho.geez': ['*.txt']}
     )
