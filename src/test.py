#!/usr/bin/env python3

"""
This file is part of the HornMorpho package.

    HornMorpho is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    HornMorpho is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with HornMorpho.  If not, see <http://www.gnu.org/licenses/>.

Author: Michael Gasser <gasser@cs.indiana.edu>
"""    
import hm.test

##### Test examples in HornMorpho2.5 Quick Reference
##
##def hm_anal():
##    for args in hm.test.ANAL:
##        hm.anal(*args)
##
##def hm_seg():
##    for args in hm.test.SEG:
##        hm.seg(*args)
##
##def hm_phon():
##    for args in hm.test.PHON:
##        hm.phon(*args)
##
##def hm_gen():
##    for args in hm.test.GEN:
##        hm.gen(*args)
##
##### Load and run particular tests
##loader = unittest.defaultTestLoader
##runner = unittest.TextTestRunner(verbosity=1)
##
##def anal_am_tam():
##    print('Running Amharic verb TAM analysis tests')
##    suite = loader.loadTestsFromName('hm.test.AnalTC.test_am_tam')
##    runner.run(suite)
##
##def anal_am_seg():
##    print('Running Amharic verb segmentation tests')
##    suite = loader.loadTestsFromName('hm.test.AnalTC.test_am_seg')
##    runner.run(suite)
##
##def anal_am_seg_tam():
##    print('Running Amharic verb TAM segmentation tests')
##    suite = loader.loadTestsFromName('hm.test.AnalTC.test_am_seg_tam')
##    runner.run(suite)
##
