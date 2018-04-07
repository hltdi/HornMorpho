"""
This file is part of HornMorpho.

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
--------------------------------------------------------------------

Author: Michael Gasser <gasser@indiana.edu>

Functions for recording and grouping analyses.
"""

from . import fs

def add_anals_to_dict(lang, analyses, knowndict, guessdict, ntokens=0, poss=[],
                      sig_feats1=None, sig_feats2=None):
    """Add analyses to dict with root as key, using 'significant' features for POS
    to organize FSs in analysis.
    """
    for analysis in analyses:
        pos = analysis[0]
        dct = guessdict if '?' in pos else knowndict
        pos = pos.replace('?', '')
        # Ignore analyses with the wrong pos
        if not poss or pos in poss:
            root = analysis[1]
            fsin = analysis[-1]
            defective = lang.morphology[pos].defective
            # Ignore a root such as verb of existence in EthSem
#            if defective and root in defective:
#                return
            if sig_feats1:
                # Create new FeatStructs to store the significant features in fsin
                fsout1 = fs.FeatStruct()
                for feat in sig_feats1:
                    if feat not in fsin:
                        continue
                    fsout1[feat] = fsin[feat]
                fsout1.freeze()
                if sig_feats2:
                    fsout2 = fs.FeatStruct()
                    for feat in sig_feats2:
                        if feat not in fsin:
                            continue
                        fsout2[feat] = fsin[feat]                    
                    fsout2.freeze()
                else:
                    fsout2 = None
            else:
                fsout1 = None

            if fsout1:
                nanal = float(len(analyses))
                typescore = 1 / nanal
                tokscore = ntokens / nanal
                if root in dct:
                    root_entry = dct[root]
                    if fsout1 not in root_entry:
                        if fsout2:
                            # Create a new dict for this combination of root and sig feats
                            dct[root][fsout1] = {fsout2: [typescore, tokscore]}
                        else:
                            dct[root][fsout1] = [typescore, tokscore]
                    elif fsout2:
                        if fsout2 not in root_entry[fsout1]:
                            # Add an entry for sig feats2 in the root sig feats dict
                            dct[root][fsout1][fsout2] = [typescore, tokscore]
                        else:
                            # Increment the score for the root/sig feats2/sig feats2 combination
                            dct[root][fsout1][fsout2][0] += typescore
                            dct[root][fsout1][fsout2][1] += tokscore
                    else:
                        dct[root][fsout1][0] += typescore
                        dct[root][fsout1][1] += tokscore
                elif fsout2:
                    # Create a new dict of dicts for this root
                    dct[root] = {fsout1: {fsout2: [typescore, tokscore]}}
                else:
                    dct[root] = {fsout1: [typescore, tokscore]}
            elif root in dct:
                dct[root].append(analysis)
            else:
                dct[root] = [analysis]
