"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2023.
    PLoGS and Michael Gasser <gasser@indiana.edu>.

    morfo is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    morfo is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with morfo.  If not, see <http://www.gnu.org/licenses/>.
--------------------------------------------------------------------
Author: Michael Gasser <gasser@indiana.edu>

Representation of 'items': words, MWEs, punctuation, numerals.
2023-09-18
"""

class Word(list):

    id = 0

    def __init__(self, init, name=''):
        '''
        init is a list of analyses returned by Language.analyze5().
        '''
        list.__init__(self, init)
#        self.posmorph = posmorph
        if not init:
            self.unk = True
        else:
            self.unk = False
        self.name = name
        self.conllu = []
        self.id = Word.id
        Word.id += 1

    def __repr__(self):
        return "W{}:{}{}".format(self.id, '*' if self.unk else '', self.name)

    def show(self):
        if len(self) == 0:
            print()
        for item in self:
            print(item)
