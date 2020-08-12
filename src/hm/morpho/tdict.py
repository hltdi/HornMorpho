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

Translation dictionaries.
Author: Michael Gasser <gasser@indiana.edu>
"""

class TDict(dict):

    def __init__(self, languages=None):
        self.languages = languages or []
        dict.__init__(self)

    def __repr__(self):
        return '<TDict {}>'.format(self.languages)

    def t(self, item, langs):
        '''Attempt to translate item into one of languages.'''
        if not isinstance(item, str):
            return item
        # The string may be missing from the dict
        lang_dict = self.get(item, {})
        # The language may be missing from the dict of translations of string
        for lang in langs:
            trans = lang_dict.get(lang)
            if trans:
                return trans
        return item

    def add(self, src, targ, lang):
        '''Association is in one direction only.'''
        if lang not in self.languages:
            self.languages.append(lang)
        item_dict = self.get(src)
        if not item_dict:
            self[src] = {}
            item_dict = self[src]
        item_dict[lang] = targ

    def tformat(self, fstring, args, langs):
        """Convert format string and args to translated string."""
        targs = [self.t(arg, langs) for arg in args]
        tfstring = self.t(fstring, langs)
        return tfstring.format(*targs)
