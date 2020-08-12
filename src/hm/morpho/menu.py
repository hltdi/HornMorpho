"""
This file is part of HornMorpho.
Copyleft (C) 2012, 2013, 2018
Michael Gasser

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

Menu for displaying and changing items in a dictionary (including
FeatStruct).

Author: Michael Gasser <gasser@indiana.edu>
"""

import sys

class DMenu:
    '''Create a menu where the user can update a dictionary based on choices in
    a list that is the basis for the menu. names is a corresponding list with
    expanded names for the elements in the list.'''

    def __init__(self, choices, names, dependencies=None):
        self.names = names
        self.choices = choices
        self.dependencies = dependencies or {}

    def __repr__(self):
        return '<DMenu {}>'.format(self.short_print())

    def short_print(self):
        feats = [x[0] for x in self.choices[:5]]
        return str(feats) + '...'

    def format(self, fstring, args, tdict=None, langs=None):
        if not tdict or not langs:
            return fstring.format(*args)
        else:
            return tdict.tformat(fstring, args, langs)

    def pretty_dict(self, dct, pretty_func=None):
        if pretty_func:
            return pretty_func(dct)
        else:
            return dct.__repr__()

    def top(self, dct, tdict=None, langs=None, repeat=True,
            pretty=None, file=sys.stdout):
        print(self.format("Current grammatical features", [], tdict=tdict, langs=langs), file=file)
        print(self.pretty_dict(dct, pretty_func=pretty), file=file)
        print(self.format("Make change to grammatical features?", [], tdict=tdict, langs=langs), file=file)
        # List of feature value pairs (new values)
        changed = []
        response = self.input('{0}:[1], {1}:[2] ', ['yes', 'no'], 2,
                              tdict=tdict, langs=langs, file=file)
        if response == 1:
            stop = False
            while not stop:
                feat, value = self.feats(dct, tdict=tdict, langs=langs,
                                         pretty=pretty, file=file)
                if feat:
                    changed.append((feat, value))
                print(self.format("Current grammatical features", [], tdict=tdict, langs=langs), file=file)
                print(self.pretty_dict(dct, pretty_func=pretty), file=file)
                print(self.format("Make another change to grammatical features?", [], tdict=tdict, langs=langs),
                      file=file)
                response = self.input('{0}:[1], {1}:[2] ', ['yes', 'no'], 2,
                                      tdict=tdict, langs=langs, file=file)
                if response == 2:
                    stop = True
        return changed

    def feat_sat_dep(self, dct, feat):
        '''Does the feat in the dictionary satisfy constraints in the dependencies?'''
        deps = self.dependencies.get(feat)
        if deps:
            for dep in deps:
                if not dct.__getitem__(tuple(dep[:-1])) ==  dep[-1]:
                    return False
        return True

    def feats(self, dct, feat=None, feat_name=None,
              choices=None, name_choices=None,
              tdict=None, langs=None,
              pretty=None, file=sys.stdout):
        if not choices: choices = self.choices
        if not name_choices: name_choices = self.names
#        for choice in choices:
#            if not self.feat_sat_dep(dct, choice[0]):
#                print('Feat', choice[0], 'is not satisfied')
        ch, nch = [], []
        for c, n_c in zip(choices, name_choices):
            if self.feat_sat_dep(dct, c[0]):
                ch.append(c)
                nch.append(n_c)
#                choices_namechoices.append((c, n_c))
        choices, name_choices = ch, nch
        print(self.format("Options", [], tdict=tdict, langs=langs), file=file)
        selections = [c[0] for c in name_choices]
        select_index = self.choose(selections,
#                                   include=include,
                                   values=False, tdict=tdict, langs=langs,
                                   file=file)
        choice = choices[select_index]
        select_feat = choice[0]
        name_choice = name_choices[select_index]
        select_feat_name = name_choice[0]
        select_values = choice[1]
        select_value_names = name_choice[1]
        print(self.format('You selected feature {0}', [select_feat_name],
                          tdict=tdict, langs=langs),
              file=file)
        if isinstance(select_values, list):
            return self.feats(dct[select_feat], select_feat, select_feat_name,
                              select_values, select_value_names,
                              tdict=tdict, langs=langs,
                              pretty=pretty, file=file)
        else:
            return self.values(dct, select_feat, select_feat_name,
                               select_values, select_value_names,
                               tdict=tdict, langs=langs,
                               pretty=pretty, file=file)

    def values(self, dct, feat, feat_name, choices, choice_names,
               tdict=None, langs=None,
               pretty=None, file=sys.stdout):
        current_value = dct[feat]
        current_value_index = choices.index(current_value)
        current_value_name = choice_names[current_value_index]

        print(self.format('Current value: {0}', [current_value_name],
                          tdict=tdict, langs=langs),
              file=file)

        choices = list(choices)
        choices.remove(current_value)
        choices.append(current_value)
        choice_names = list(choice_names)
        choice_names.remove(current_value_name)
        choice_names.append(current_value_name)

        select_index = self.choose(choice_names, values=True,
                                   tdict=tdict, langs=langs, file=file)
        if select_index == len(choice_names) - 1:
            # Selected no change
            print(self.format('You chose to make no change', [],
                              tdict=tdict, langs=langs))
            return None, None

        choice = choices[select_index]
        choice_name = choice_names[select_index]

        print(self.format('You selected value {0} for {1}', [choice_name, feat_name],
                          tdict=tdict, langs=langs),
              file=file)
        # Update the dictionary
        dct[feat] = choice
        return feat, choice

    def choose(self, choices, include=None, values=False, tdict=None, langs=None, file=sys.stdout):
        choice = None
        include = include or []
        nchoices = len(choices)
        for index, option in enumerate(choices[:-1] if values else choices):
            print(self.format('[{0}] {1}', [index+1, option], tdict=tdict, langs=langs),
                  file=file)
        if values:
            last_choice = choices[-1]
            print(self.format('[{0}] Keep value at {1}', [index+2, last_choice],
                              tdict=tdict, langs=langs),
                  file=file)
        print(file=file)
        choice = self.input('{0}: ', ['Selection'], nchoices,
                            tdict=tdict, langs=langs, file=file)
        return choice - 1

    def input(self, prompt, args, nchoices, tdict=None, langs=None, file=sys.stdout):
        answer = None
        while not answer:
            response = input(self.format(prompt, args, tdict=tdict, langs=langs))
            if not response.isdigit():
                print(self.format('Please enter a digit between 1 and {0}', [nchoices],
                                  tdict=tdict, langs=langs),
                      file=file)
            else:
                resp_int = int(response)
                if resp_int > nchoices or resp_int < 1:
                    print(self.format('Please enter a digit between 1 and {0}', [nchoices],
                                      tdict=tdict, langs=langs),
                          file=file)
                else:
                    answer = resp_int
        return answer
