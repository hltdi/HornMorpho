"""
This file is part of the HornMorpho package.

Copyright (C) 2023.
Michael Gasser <gasser@indiana.edu>

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
-------------------------------------------------------
Creating an FST for a set of templates.
2023.01.14.

"""

import re, os
from .utils import segment
from .semiring import FSSet, UNIFICATION_SR, TOPFSS
from .fs import FeatStructParser
from .geez import *

# Default name for final state
DFLT_FINAL = 'fin'

class Template:

    PARSER = FSSet.parse
    TEMPLATE_RE = re.compile(r'\s*(.+)$')
    FEATURES_RE = re.compile(r'\s*(\[.+\])$')
    CONSTRAINT_RE = re.compile(r'\s*%(.+)$')

    EMPTY_CHAR = '-'

#    def __init__(self, fst, directory=''):
#        self.fst = fst
#        self.cascade = fst.cascade
#        self.seg_units = self.cascade.seg_units
#        self.directory = directory
#        self.weighting = UNIFICATION_SR
#        self.states = []

#    def __repr__(self):
#        return "Roots {}".format(self.fst.label)

    @staticmethod
    def make_template_states(fst, template, index, features, constraints, cascade):

#        if constraints:
#            constraint_feats = "[{}]".format(','.join(constraints))
#            constraint_weight = UNIFICATION_SR.parse_weight(features)
#        else:
#            constraint_weight = None

        weight = UNIFICATION_SR.parse_weight(features)
        
        print("*** Making template states for template {}: {} : {}".format(index, template, weight.__repr__()))

        template_name = "tmp{}".format(index)

        states = []

        template = template.split()

        tmp_length = len(template)

        # Position of possibly geminated consonant (all EES!)
        gem_pos = tmp_length - 1

        for elemindex, charset in enumerate(template):
            position = elemindex + 1
            if charset == Template.EMPTY_CHAR:
                # No character in this position; skip to next position
                continue
            gem_feat = None
            if position == gem_pos:
                # this is where the geminated character might be
                gem_feat = "gem{}".format(gem_pos)
                gem = ':' in charset
                if gem:
                    gem_feat = UNIFICATION_SR.parse_weight("[+{}]".format(gem_feat))
                    charset = charset.replace(':', '')
                else:
                    gem_feat = UNIFICATION_SR.parse_weight("[-{}]".format(gem_feat))
            state_name = "{}_{}".format(template_name, position)
            states.append((state_name, charset, gem_feat))

        source = 'start'
        for index, (dest, charset, gem_feat) in enumerate(states[:-1]):
            if not fst.has_state(dest):
                fst.add_state(dest)
            wt=None
            if index==0:
                wt = weight
            elif gem_feat:
                wt = gem_feat
            fst.add_arc(source, dest, charset, charset, weight=wt)
            source = dest

        last_state, charset, gem_feat = states[-1]
#        if not fst.has_state(source):
#            fst.add_state(source)
        fst.add_arc(source, 'end', charset, charset)

    @staticmethod
    def parse(label, s, cascade=None, fst=None, gen=False, 
              directory='', seg_units=[], abbrevs=None,
              weight_constraint=None, verbose=False):
        """
        Parse an FST from a string consisting of multiple lines from a file.
        Create a new FST if fst is None.
        """
#        print("** Parsing template file {}, fst {}".format(s, fst))

#        weighting = fst.weighting()

        templates = []

        current_features = []

        current_constraints = []

        # Create start and end states
        if not fst.has_state(label): fst.add_state('start')
        fst._set_initial_state('start')
        if not fst.has_state('end'): fst.add_state('end')
        fst.set_final('end')

        lines = s.split('\n')[::-1]

        while lines:
            line = lines.pop().split('#')[0].strip() # strip comments

            if not line: continue

            m = Template.FEATURES_RE.match(line)
            if m:
                features = m.groups()[0]
                current_features.append(features)
                continue

            m = Template.CONSTRAINT_RE.match(line)
            if m:
                constraints = m.groups()[0]
                print("*** constraints {}".format(constraints))
                current_constraints.append(constraints)
                continue

            m = Template.TEMPLATE_RE.match(line)
            if m:
                template = m.groups()[0]
                print("*** template {}".format(template))
                current_features = ';'.join(current_features)
                templates.append((template, current_features, current_constraints))
                current_features = []
                current_constraints = []
                continue

            print("*** Something wrong with {}".format(line))

        for index, (template, features, constraints) in enumerate(templates):
            Template.make_template_states(fst, template, index+1, features, constraints, cascade)

        print(fst)
        return fst



