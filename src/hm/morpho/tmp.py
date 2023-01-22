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
from .utils import segment, allcombs
from .semiring import FSSet, UNIFICATION_SR, TOPFSS
from .fs import FeatStruct, simple_unify
#from .fs import FeatStructParser
from .geez import *

# Default name for final state
DFLT_FINAL = 'fin'

class Template:

    PARSER = FSSet.parse
    TEMPLATE_RE = re.compile(r'\s*(.+)$')
    FEATURES_RE = re.compile(r'\s*(\[.+\])$')
    MAIN_CONSTRAINT_RE = re.compile(r'\s*%%(.+)$')
    CONSTRAINT_RE = re.compile(r'\s*%(.+)$')
    INVENTORY_RE = re.compile(r'\s*\$\s*(.+)$')

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
    def make_template_states(fst, template, index, features, constraints, strong_inventory, cascade):

#        if constraints:
#            constraint_feats = "[{}]".format(','.join(constraints))
#            constraint_weight = UNIFICATION_SR.parse_weight(features)
#        else:
#            constraint_weight = None

        # Add constraints to all features
        if constraints:
            constraints = ','.join(constraints)
            for i, feature in enumerate(features):
                features[i] = "{},{}]".format(feature[:-1], constraints)

        features = ';'.join(features)

        weight = UNIFICATION_SR.parse_weight(features)

        cls = weight.get('c')

#        print("*** Making template states for template {}: {} : {}".format(index, template, weight.__repr__()))

        template_name = "tmp{}".format(index)

        states = []

        template = template.split()

        strong_feats = [w for w in list(weight) if w.get('strong')]

        if strong_feats:
            print("** FSs for {}: {}".format(template, strong_feats))

        inventory = strong_inventory.get(cls)

        for inv_feats in inventory.keys():
            if any([simple_unify(inv_feats, f) != 'fail' for f in strong_feats]):
                inventory[inv_feats].append(template)
        
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
#            print("** Making states {} {} {} {}".format(index, dest, charset, gem_feat))
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
        fst.add_arc(source, 'end', charset, charset, weight=gem_feat)

    @staticmethod
    def expand_inventory(classes, features):
        inventory1 = allcombs(features)
        inventory1 = ["[" + ','.join(f) + "]" for f in inventory1]
        inventory1 = dict([(FeatStruct(f, freeze=True), []) for f in inventory1])
        inventory = dict([(c, inventory1.copy()) for c in classes])
        print("** inventory expanded {}".format(inventory))
        return inventory

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

        current_main_constraints = []

        current_constraints = []

        inventory_classes = []

        weak_inventory_classes = []

        inventory = []

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

            m = Template.INVENTORY_RE.match(line)
            if m:
                inventory1 = m.groups()[0]
                print("*** inventory item {}".format(inventory1))
                f, values = inventory1.split('=')
                if f in ('c', 'cls', 'class'):
                    # These are root classes; make a separate dict for each
                    inventory_classes = values.split('|')
                else:
                    values = values.split('|')
                    inv = ["{}={}".format(f, v) for v in values]
                    inventory.append(inv)
                continue

            m = Template.MAIN_CONSTRAINT_RE.match(line)
            if m:
                constraints = m.groups()[0]
                # reset main constraints
                current_main_constraints = [constraints]
#                print("*** main constraints {}".format(constraints))
#                current_main_constraints.append(constraints)
                continue

            m = Template.CONSTRAINT_RE.match(line)
            if m:
                # Each of these should represent a new weak subclass
                constraints = m.groups()[0]
                print("*** constraints {}".format(constraints))
                current_constraints.append(constraints)
                continue

            m = Template.TEMPLATE_RE.match(line)
            if m:
                template = m.groups()[0]
#                print("*** template {}".format(template))
                templates.append((template, current_features, current_main_constraints + current_constraints))
                current_features = []
                current_constraints = []
                continue

            print("*** Something wrong with {}".format(line))

        inventory = Template.expand_inventory(inventory_classes, inventory)

        for index, (template, features, constraints) in enumerate(templates):
            Template.make_template_states(fst, template, index+1, features, constraints, inventory, cascade)

        print("*** inventory {}".format(inventory.get('A')))

#        print(fst)
        return fst



