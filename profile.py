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

Copyleft, 2018, Michael Gasser <gasser@indiana.edu>
"""

import hm
import cProfile
import pstats

def profile(call, file="prof.txt"):
    cProfile.run(call, file)
    p = pstats.Stats(file)
    p.sort_stats('time').print_stats(20)

if __name__ == "__main__":
    print("Loading Amharic")
    hm.load_lang('am', load_morph=False, guess=False, verbose=True)
    AM = hm.morpho.get_language('am', verbose=True)
    print("Analyzing yeteseberew 1")
    profile("AM.anal_word('yeteseberew')")
    print("Analyzing yeteseberew 2")
    profile("AM.anal_word('yeteseberew')")
    print("Recompiling Amharic verb FSTs")
    AMV = AM.morphology['v']
    profile("AMV.load_fst(True, compose_backwards=False, verbose=True)")


