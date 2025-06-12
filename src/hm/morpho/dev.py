"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2017, 2018.
    PLoGS and Michael Gasser <gasser@iu.edu>.

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

2017.05.08
-- Created.
"""

import os

LANGUAGE_DIR = os.path.join(os.path.dirname(__file__),
                            os.path.pardir, 'languages')

class Developer:
    """Just a container for methods used for creating an FST for a new language."""

    def __init__(language, lang_abbrev, POSs):
        """Given some basic data, create the directories and some of the files needed for building
        the FSTs for a new language."""
        self.language = language
        self.lang_abbrev = lang_abbrev
        self.POSs = POSs

    def create_dirfiles(self):
        """Create the directories and basic files needed for the language."""
    

