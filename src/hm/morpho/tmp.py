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
from .semiring import FSSet
from .fs import FeatStruct, simple_unify
from .geez import *
from .ees import EES, TARGET_WT_CONV

#REG_FS = FSSet("[+reg]")

# Default name for final state
DFLT_FINAL = 'fin'

make_weight = EES.make_weight
conv_string = EES.conv_string

class Template:

#    PARSER = FSSet.parse
    TEMPLATE_RE = re.compile(r'\s*(.+)$')
    FEATURES_RE = re.compile(r'\s*(\[.+\])$')
    MAIN_CONSTRAINT_RE = re.compile(r'\s*%%(.+)$')
    CONSTRAINT_RE = re.compile(r'\s*%(.+)$')
    INVENTORY_RE = re.compile(r'\s*\$\s*(.+)$')

    CHAR_SET_RE = re.compile(r'\s*\$\$\s*(.+?)\s+(.+?)$')

    EMPTY_CHAR = '-'

    @staticmethod
    def make_template_feats(constraints, templength):
        '''
        constraints is something like 1=እ or 1=እ,3=ይ.
        '''
        feats = []
        if constraints:
            constraints = [c.split('=') for c in constraints.split(',')]
            constraints = dict([(int(f), v) for f, v in constraints])
        else:
            constraints = {}
        for i in range(templength):
            if i+1 in constraints:
                feats.append("{}={}".format(i+1, constraints[i+1]))
            else:
                feats.append("{}=X".format(i+1))
        return ','.join(feats)

    @staticmethod
    def expand_weak_constraint(constraint, char_sets):
        '''
        Constraint may contain an abbreviation like L, in which case it's expanded.
        '''
        for label, char_set in char_sets.items():
            if label in constraint:
                constraint = constraint.replace(label, char_set)
        return constraint

    @staticmethod
    def make_all_template_states(fst, tmp_dict, default_final, gen=False):
        '''
        Add states and arcs for all templates in the template dict.
        '''
        # Create final default state and arc to end state
        if not fst.has_state('final'): fst.add_state('final')
        fst.add_arc('final', 'end', default_final, default_final)
#        print("*** Created state from final to end with chars {}".format(default_final))
            
        for index, (template, weight) in enumerate(tmp_dict.items()):
            template_name = "tmp{}".format(index)
            states = []
            tmp_length = len(template)
            # Position of possibly geminated consonant (all EES!)
            gem_pos = {tmp_length - 1, tmp_length - 2}

            for elemindex, charset in enumerate(template):
                gem = ':' in charset or EES.pre_gem_char in charset
                position = elemindex + 1
                if charset == Template.EMPTY_CHAR:
                    # No character in this position; skip to next position
                    continue
                gem_feat = None
#                featname = "gem" if gen else "sgem"
                if position in gem_pos:
                    # this is where the geminated character might be
                    gem_feat = "gem{}".format(position)
                    if gem:
                        gem_feat = make_weight("[+{}]".format(gem_feat), target=gen)
#                        gem_feat = UNIFICATION_SR.parse_weight("[+{}]".format(gem_feat))
                        charset = charset.replace(':', '')
                    else:
                        gem_feat = make_weight("[-{}]".format(gem_feat), target=gen)
#                        gem_feat = UNIFICATION_SR.parse_weight("[-{}]".format(gem_feat))
                state_name = "{}_{}".format(template_name, position)
                states.append((state_name, charset, gem_feat, gem))

#            print("** final default {}".format(default_final))
            source = 'start'
            if states[-1][1] == default_final and template[-1] != '-':
#                print(" *** template {} has final default; states {}".format(template, states))
                # template ends in default final, so use existing final arc
                states_to_create = states[:-2]
                last_state = states[-2]
                end = 'final'
            else:
                # template ends in some other character set, so create the final arc to 'end'
                states_to_create = states[:-1]
                last_state = states[-1]
                end = 'end'

            for index, (dest, charset, gem_feat, gem) in enumerate(states_to_create):
#                print("** state {} gfeat {} gem {}".format(dest, gem_feat.__repr__(), gem))
                if not fst.has_state(dest):
                    fst.add_state(dest)
                wt=None
                if index==0:
                    wt = weight
                elif gem_feat:
                    wt = gem_feat
                fst.add_arc(source, dest, charset, charset, weight=wt)
                source = dest
                
            state, charset, gem_feat, gem = last_state
            if not states_to_create:
                # This is the only arc for this template, so it needs the full weight
                wt = weight
            else:
                wt = gem_feat
            if gem:
                # Make a separate arc for the pre-gem character
                dest0 = source + '_gem'
                fst.add_state(dest0)
                c = EES.pre_gem_char
                fst.add_arc(source, dest0, c, c, weight=wt)
                fst.add_arc(dest0, end, charset, charset, weight=wt)
            else:
                fst.add_arc(source, end, charset, charset, weight=wt)

    @staticmethod
    def add_template(fst, template, index, features, constraints, tmp_dict=None,
                     strong_inventory=None, weak_inventory=None, subclass='', cascade=None,
                     gen=False, char_sets=None):
        """
        Update strong or weak inventory and template dict.
        """
            
#        print("*** Making states for {} : {}; constraints {}".format(template, features, constraints))

        # Add constraints to all features
        if constraints:
            mainconstraint, weakconstraint = constraints
            template_feats = Template.make_template_feats(weakconstraint, len(template))
            weakconstraint = Template.expand_weak_constraint(weakconstraint, char_sets)
            constraints = "{},{},tmp=[{}]".format(mainconstraint, weakconstraint, template_feats)
            for i, feature in enumerate(features):
                features[i] = "{},{}]".format(feature[:-1], constraints)

        features = ';'.join(features)
        weight = make_weight(features, target=gen)
        cls = weight.get('tc') if gen else weight.get('c')
        strong_feat = 'tstrong' if gen else 'strong'
        strong = weight.get(strong_feat)

        inventory = strong_inventory.get(cls)

        if strong:
            strong_feats = [w for w in list(weight) if w.get(strong_feat)]
            for inv_feats in inventory.keys():
                if any([simple_unify(inv_feats, f) != 'fail' for f in strong_feats]):
                    inventory[inv_feats].append(template)
        else:
            weak_feats = [w for w in list(weight) if not w.get(strong_feat)]
            weak_subinventory = weak_inventory[cls][subclass]
            for inv_feats in inventory.keys():
                if any([simple_unify(inv_feats, f) != 'fail' for f in weak_feats]):
                    if inv_feats not in weak_subinventory:
                        weak_subinventory[inv_feats] = []
                    weak_subinventory[inv_feats].append(template)

        if template in tmp_dict:
            tmp_dict[template] = tmp_dict[template].union(weight)
        else:
            tmp_dict[template] = weight

    @staticmethod
    def expand_inventory(classes, features, gen=False):
        inventory1 = ["[" + ','.join(f) + "]" for f in allcombs(features)]
        if gen:
            inventory1 = [conv_string(i, TARGET_WT_CONV) for i in inventory1]
        inventory = dict([(c, dict([(FeatStruct(f, freeze=True), []) for f in inventory1])) for c in classes])
        return inventory

    @staticmethod
    def make_weak_inventory(weak_classes, inventory):
        inv = {}
        for cls, subclass in weak_classes:
            if cls not in inv:
                inv[cls] = {}
            inv[cls][subclass] = {}
        return inv

    @staticmethod
    def complete_weak_inventory(weak_inventory, strong_inventory, tmp_dict, weak_constraints, gen=False):
        '''
        Go through each weak subclass and see which feature sets in the strong inventory
        don't have templates yet. Assign the strong templates for these features sets
        to the weak subclasses unless a feature (set) in the list of weak_constraints for the subclass.
        '''
#        print("** Completing weak inventory")
        for cls, features in strong_inventory.items():
            weak_class_inventory = weak_inventory.get(cls)
            weak_class_constraints = weak_constraints.get(cls)
            if weak_class_inventory:
                for feature, templates in features.items():
                    if not templates:
                        # No templates for this feature set in the strong inventory
                        continue
#                    print("** STRONG TEMPLATES {}, feature {}".format(templates, features.__repr__()))
                    for subclass, weak_features in weak_class_inventory.items():
#                        print("  ** strong template {}; subclass {}, weakfeats {}, feature {}".format(templates, subclass, weak_features, feature.__repr__()))
                        # Look for templates with feature
                        found = False
                        for weak_feature, weak_templates in weak_features.items():
                            if simple_unify(weak_feature, feature) != 'fail':
#                                print ("   *** unified weakfeat {} with feat {}; continuing".format(weak_feature.__repr__(), feature.__repr__()))
                                found = True
                                break
                        if not found:
#                            print("   *** {} failed to unify with {}".format(feature.__repr__(), weak_features.__repr__()))
#                            print("   *** subclass {}".format(subclass))
                            weak_subclass_constraints = weak_class_constraints.get(subclass) if weak_class_constraints else None
#                            if weak_subclass_constraints:
#                                print("*** No template for {} in subclass {}".format(feature.__repr__(), subclass))
#                                print("*** weak constraints {}".format(weak_subclass_constraints))
                            prevented = False
                            if weak_subclass_constraints:
                                for weak_constraint in weak_subclass_constraints:
                                    if simple_unify(feature, weak_constraint) != 'fail':
#                                        print("  *** weak constraint matches; prevented!")
                                        prevented = True
                                        break
                            if prevented:
                                continue
                            # There may be more than one positional constraint
                            # Create the weak feature set (add -strong, the class, e.g., c=A, and the subclass, e.g., 2=ው)
                            strength_feat = 'tstrong' if gen else 'strong'
                            cls_feat = 'tc' if gen else 'c'
                            new_weak_feats = feature.copy()
                            new_weak_feats[strength_feat] = False
                            new_weak_feats[cls_feat] = cls
                            subclass_feats = [sc.split('=') for sc in subclass.split(',')]
                            for feat, value in subclass_feats:
                                if '|' in value:
                                    nwf = []
                                    for v in value.split('|'):
                                        n = new_weak_feats.copy()
                                        n[feat] = v
                                        nwf.append(n)
                                    new_weak_feats = nwf
                                else:
                                    new_weak_feats[feat] = value
                            new_weak_feats = FSSet(new_weak_feats)
#                            print("  **** Creating weak feature: {}".format(new_weak_feats.__repr__()))
                            # Pick first template for this feature set for the weak subclass
                            for template in templates:
#                            template = templates[0]
                                tmp_dict[template] = tmp_dict[template].union(new_weak_feats)
#                            print("  **** new tmp dict for template {}: {}".format(template, tmp_dict[template]))

    @staticmethod
    def copy_templates(features, sourceclass, strong_inventory, tmp_dict, gen=False):
#        print("** class inventory")
#        print("{}".format(strong_inventory.get(sourceclass)))
        clsfeat = 'tc' if gen else 'c'
        strengthfeat = 'tstrong' if gen else 'strong'
        destfeatures = FeatStruct("[" + features + "]")
        destclass = destfeatures.get('c')
        matchfeats = destfeatures.delete(['c', 'strong'])
        source_inventory = strong_inventory.get(sourceclass)
        dest_inventory = strong_inventory.get(destclass)
#        print("** Copy templates for {} from {}, matchfeats {}".format(destfeatures.__repr__(), sourceclass, matchfeats.__repr__()))
        for features, templates in source_inventory.items():
            if templates and simple_unify(features, matchfeats) != 'fail':
                dest_inventory[features] = templates
                destfeats1 = features.copy()
                destfeats1[strengthfeat] = True
                destfeats1[clsfeat] = destclass
                destfeats1 = FSSet(destfeats1)
#                print("  *** Match: {} / {}, newfeats {}".format(features.__repr__(), templates, destfeats1.__repr__()))
                for template in templates:
                    tmp_dict[template] = tmp_dict[template].union(destfeats1)
             
    @staticmethod
    def get_class(features):
        '''
        Get the class from an expression like "[c=A,a=0]", not an actual FeatStruct.
        '''
        features = features.replace("[", '').replace("]", '')
        features = features.split('c=')
        for x in features[1:]:
            c = x.split(',')[0]
            if c:
                # Assume there is one class
                return c
        return ''

    @staticmethod
    def add_weak_constraint(subclass, features, constraint_dict, gen=False):
        '''
        Add a constraint for the subclass to not have any templates for features.
        '''
        features = FeatStruct("[" + features + "]", freeze=False)
        cls_feat = 'tc' if gen else 'c'
        strength_feat = 'tstrong' if gen else 'strong'
        cls = features.get(cls_feat)
        features = features.delete([cls_feat, strength_feat])
#        print("*** Adding constraint for class {}, subclass {}, features {}".format(cls, subclass, features.__repr__()))
        if cls not in constraint_dict:
            constraint_dict[cls] = {}
        if subclass not in constraint_dict[cls]:
            constraint_dict[cls][subclass] = []
        constraint_dict[cls][subclass].append(features)

    @staticmethod
    def parse(label, s, cascade=None, fst=None, gen=False, seglevel=2,
              directory='', seg_units=[], abbrevs=None,
              weight_constraint=None, verbose=False):
        """
        Parse an FST from a string consisting of multiple lines from a file.
        Create a new FST if fst is None.
        """

        language = cascade.language
        pos = cascade.pos
        posmorph = language.morphology.get(pos)

#        print("** Parsing template file; fst {}; cascade {}, POS {}".format(fst, cascade, cascade.pos))

        templates = []
        tmp_dict = {}
        current_features = []
        current_main_constraints = []
        current_constraints = ''
        inventory_classes = []
        weak_inventory_classes = []
        current_class = ''
        current_subclass = ''
        inventory = []
        template_dict = {}
        copy_templates = []
        weak_constraints = {}

        char_sets = {}

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

            m = Template.CHAR_SET_RE.match(line)
            if m:
                charset, chars = m.groups()
#                print("*** charset {}: {}".format(charset, chars))
                char_sets[charset] = chars
                continue

            m = Template.INVENTORY_RE.match(line)
            if m:
                inventory1 = m.groups()[0]
#                print("*** inventory item {}".format(inventory1))
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
                if '==' in constraints:
                    features, sourceclass = constraints.split('==')
                    features = features.strip()
                    sourceclass = sourceclass.strip()
                    copy_templates.append((features, sourceclass))
                    continue
                # reset main constraints
                current_constraints = ''
                current_subclass = ''
                current_main_constraints = [constraints]
#                print("*** main constraints {}".format(constraints))
                current_class = Template.get_class(constraints)
#                current_main_constraints.append(constraints)
                continue

            m = Template.CONSTRAINT_RE.match(line)
            if m:
                # Each of these should represent a new weak subclass within the current feature set (normally values for a and c)
                constraints = m.groups()[0]
#                print("** weak constraints {}".format(constraints))
                if '!' in constraints:
                    subclass = constraints.replace('!', '').strip()
                    Template.add_weak_constraint(subclass, current_main_constraints[0], weak_constraints, gen=gen)
                    continue
                if gen:
                    # precede position ints with 't'
                    constraints = constraints.split(',')
                    constraints = ['t' + c for c in constraints]
                    constraints = ','.join(constraints)

#                constraint_feat = Template.make_weakclass_feat(constraints)
#                print("*** current class {} constraints {}".format(current_class, constraint_feat.__repr__()))
                weak_inventory_classes.append((current_class, constraints))
                current_constraints = constraints
                current_subclass = constraints
                continue

            m = Template.TEMPLATE_RE.match(line)
            if m:
                template = m.groups()[0]
                template = tuple(template.split())
#                print("*** Adding template {}, current_features {}, constraints {}, subclass {}".format(template, current_features, current_main_constraints + [current_constraints], current_subclass))
                templates.append((template, current_features, current_main_constraints + [current_constraints], current_subclass))
                current_features = []
                continue

            print("*** Something wrong with {}".format(line))

        inventory = Template.expand_inventory(inventory_classes, inventory, gen=gen)

        weak_inventory = Template.make_weak_inventory(weak_inventory_classes, inventory)

        # Find most common final character set.
        finals = {}
        for template, x, y, z in templates:
            final = template[-1]
            if final in finals:
                finals[final] += 1
            else:
                finals[final] = 1
        finals = list(finals.items())
        finals.sort(key=lambda x: x[1], reverse=True)
#        print("*** finals {}".format(finals))
        default_final = finals[0][0]

        for index, (template, features, constraints, subclass) in enumerate(templates):
            Template.add_template(fst, template, index+1, features, constraints, tmp_dict=tmp_dict,
                                  strong_inventory=inventory, weak_inventory=weak_inventory,
                                  subclass=subclass, cascade=cascade, gen=gen, char_sets=char_sets)

        for features, sourceclass in copy_templates:
            Template.copy_templates(features, sourceclass, inventory, tmp_dict, gen=gen)

        Template.complete_weak_inventory(weak_inventory, inventory, tmp_dict, weak_constraints, gen=gen)

#        for x, y in weak_inventory.get('A').get('3=እ').items():
#            print("***** {}, {}".format(x.__repr__(), y))

#        print("*** weak inventory {}".format(weak_inventory.get('A').get('3=እ')))

#        print("*** inventory {}".format(inventory.get('A')))
#        print("*** weak inventory {}".format(weak_inventory))

        Template.make_all_template_states(fst, tmp_dict, default_final, gen=gen)

#        print("*** tmp_dict <*e *: *> {}".format(tmp_dict.get(('*e', '*:', '*'))))

#        print(fst)
        return fst



