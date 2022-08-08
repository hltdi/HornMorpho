"""
This file is part of HornMorph (and morfo), which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2019, 2022.
    PLoGS and Michael Gasser <gasser@indiana.edu>.

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

Simple alternation rules for realizing sequences of morphemes.
Called in language-specific functions following segmentation.
"""

import re

class Rules(list):
    """An ordered list of rules, sharing classes of segments."""

    def __init__(self, language=None, seg_units=None):
        if seg_units:
            self.seg_units = seg_units
        elif language:
            self.seg_units = language.seg_units
        else:
            print("Warning: can't create Rules without seg_units")
        self.segments = []
        self.segments.extend(self.seg_units[0])
        for values in self.seg_units[1].values():
            self.segments.extend(values)
        self.classes = {}

    def add_class(self, label, segments):
        self.classes[label] = Rule.segments2RE(segments)

    def add(self, rule):
        self.append(rule)

    def add_rules(self, rules):
        self.extend(rules)

    def apply(self, string):
        for rule in self:
            string = rule.apply(string)
        return string

    @staticmethod
    def segments2RE(segments):
        """Convert a list of segments, including possibly some with multiple
        characters to a RE string representing a single instance."""
        single = ''
        multiple = []
        for segment in segments:
            if len(segment) == 1:
                single += segment
            else:
                multiple.append(segment)
        if single:
            single = "[" + single + "]"
        if multiple:
            multiple = "|".join(multiple)
        if single and multiple:
            return single + "|" + multiple
        else:
            return single or multiple

class Rule:

    def __init__(self, pattern, repl):
        self.pattern = pattern
        self.repl = repl

    def apply(self, string):
        return re.sub(self.pattern, self.repl, string)

    @staticmethod
    def group(string):
        """Make string into a RE group if it isn't one already."""
        if string and string[0] != "(":
            return "(" + string + ")"
        return string

class Repl(Rule):

    def __init__(self, pre='', inter1='', replpart='', inter2='', post='', replacement=''):
        index = 1
        pattern = ''
        repl = r''
        if pre:
            pattern += Rule.group(pre)
            repl += "\{}".format(index)
            index += 1
        if inter1:
            pattern += Rule.group(inter1)
            repl += "\{}".format(index)
            index += 1
        pattern += replpart
        repl += replacement
        if inter2:
            pattern += Rule.group(inter2)
            repl += "\{}".format(index)
            index += 1
        if post:
            pattern += Rule.group(post)
            repl += "\{}".format(index)
        self.pattern = pattern
        self.repl = repl

class SimpRepl(Repl):

    def __init__(self, replpart='', replacement=''):
        Repl.__init__(self, replpart=replpart, replacement=replacement)

class Insert(Repl):

    def __init__(self, pre="", post="", insertion=""):
        Repl.__init__(self, pre=pre, replpart = "", post=post, replacement=insertion)

class Del(Repl):

    def __init__(self, pre='', delpart='', post=''):
        Repl.__init__(self, pre=pre, replpart=delpart, post=post, replacement='')

class Assim(Rule):

    def __init__(self, dct, pre='', inter='', post='', prog=True, replace=False):
        segments = ''.join(dct.keys())
        ngroups = 2
        if prog:
            pre = Rule.group("[{}]".format(segments))
            post = Rule.group(post)
        else:
            post = Rule.group("[{}]".format(segments))
            pre = Rule.group(pre)
        if inter:
            inter = Rule.group(inter)
        self.pattern = pre + inter + post
        self.repl = AssimFunc(dct, prog=prog, inter=inter, replace=replace)

class AssimFunc:

    def __init__(self, dct, inter='', prog=True, replace=False):
        """dct is a segment dictionary giving replacements for segments
        when the rule applies.
        prog is a boolean specifying whether the rule is progressive (or regressive).
        replace is a boolean specifying whether the unchanged segment is deleted.
        inter is True (or something else) if there's an intermediary group.
        """
        self.dct = dct
        self.prog = prog
        self.replace = replace
        self.inter = inter

    def __call__(self, matchobj):
        m1 = matchobj.group(1)
        m2 = matchobj.group(3 if self.inter else 2)
        minter = None
        if self.inter:
            minter = matchobj.group(2)
        if self.prog:
            changed = self.dct[m1]
            if self.inter:
                changed += minter
            if not self.replace:
                changed += m2
            return changed
        else:
            if not self.replace:
                changed = m1
            if self.inter:
                changed += minter
            changed += self.dct[m2]
            return changed
