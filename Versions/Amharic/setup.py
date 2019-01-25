#!/usr/bin/env python3

import sys

from distutils.core import setup

setup(name='HornMorphoA',
      version='3.1',
      description='Morphological analyzer for Amharic',
      author='Michael Gasser',
      author_email='gasser@indiana.edu',
      url='http://homes.soic.indiana.edu/gasser/plogs.html',
      license="GPL v3",
      packages=['hm', 'hm.morpho', 'hm.morpho.geez'],
      package_data = {'hm': ['languages/am/cas/*.cas',
                             'languages/am/fst/*.fst',
                             'languages/am/lex/*.lex',
                             'languages/am/stat/*.dct',
                             'languages/am/cache/am.cch',
                             'languages/am/data/ag.txt'],
                      'hm.morpho.geez': ['am_conv_sera.txt', 'ti_conv_sera.txt', 'stv_conv_sera.txt']}
     )
