#!/usr/bin/env python3

"""
This file is part of the L3Morpho package.

    L3Morpho is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    L3Morpho is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with L3Morpho.  If not, see <http://www.gnu.org/licenses/>.

Author: Michael Gasser <gasser@cs.indiana.edu>
"""

import l3
import unittest

GUARANI = \
    ["ndoguatái", "oñeñapytĩva", "noñemoĝuahẽiva'ekue", "nakarãíri",
     "chera'arõ", "hemby", "nemoíri", "ñamboryrýi", "nañamboryrýiri",
     "ndoúi"]

# Examples from HornMorpho 2.5 Quick Reference
ANAL = [('ti', 'ናብ'), ('ti', 'ፔፕሲ'), ('ti', 'ብዘጋጥመና'), ('ti', 'ዘየብለይ'),
        ('om', 'afeeramaniiru'), ('om', 'dubbanne'),
        ('am', 'የማያስፈልጋትስ'), ('am', 'አይደለችም'),
        ('am', 'ቢያስጨንቁአቸው'),
        ('am', 'ለዘመዶቻችንም'),
        ('am', 'ይመጣሉ')]

SEG = [('am', 'ሲያጭበረብሩን'), ('om', 'afeeramaniiru')]

PHON = [('am', "ይመታሉ")]

GEN = [('am', "mWl'"),
       ('am', "mWl'", '[sb=[+p2,+fem],ob=[+plr,+l]]'),
       ('am', "mengst", '[+plr,+def]'), ('am', 'sdb', '[pos=n,v=agt,vc=cs,as=rc]'),
       ('am', 'brkt', '[pos=n,v=ins,pp=ke,cnj=m,+def]'),
       ('am', 'ne', '[+neg, sb=[+p1,+plr]]'),
#       ('am', 'kongo', '[pp=be]', guess=True),
       ('am', 'wdd_r', '[+gen, poss=[+p1,+plr]]'),
       ('om', 'sirb'), ('om', 'sirb', '[sb=[+fem],tm=prf]'),
       ('om', 'barbaad', '[+inf,cnj=f]'),
       ('om', 'sob', '[der=[+autoben],sb=[+p2],+neg,tm=prs]'),
       ('ti', "gWyy"),
       ('ti', 'HSb', '[sb=[+p2,+fem],ob=[+plr]]'),
       ('ti', 'n|qTqT', '[vc=ps,tm=imf,sb=[+p1,+plr]]'),
       ('ti', 'gdf','[tm=j_i,+neg,sb=[+p2],ob=[+plr],vc=ps,as=rc]')]

AMHARIC = \
    ["'aweTa", "'aweTahu", "'aweTah", "'aweTax", "'aweTac", "'aweTan", "'aweTachu", "'aweTu",
     "'alaweTum", "'ndalaweTac",
     "'ndaweTu", "'aweTahWacew", "'aweTahew", "kaweTanew", "yaweTac", "tawCalex",
     "yemayaweTa", "sayaweTWachu", "'ndalaweTa",
     "yaweTa", "'aweTalehu", "yemaweTa", "bemiyaweTaw", "yemtaweTat",
     "'awTtot", "'awTcalehu", "'awTtalec", "'awTtewnal",
     "'awCi", "'atawTut", "'ayamTWat", "yawTu"]

AMH_TAM = \
    ["sebere", "ysebral", "sber", "sebro", "tesabere", "ysaberal",
     "'asabere", "sebabere", "ysebaberal", "'asebabere",
     "qeyere", "yqeyral", "qeyr", "qeyro",
     "TafeTe", "yTafTal", "TafT", "TafTo", "yTafeTal", "'asTafeTe", "teTafTWal",
     "CebeCebe", "CebCbo", "yCebeCebal",
     "'aleqe", "'leq", "'astelaleqe", "'alqo", "taleqe",
     "'ageze", "'agz", "yagzal",
     "cale", "yclal", "cal", "clo", "cacale",
     "geba", "ygebal", "gba", "gebto", "tegabac", "'agebabten", "ygbabal",
     "'agbabanacew", "tegbabtew", "'agbabtew",
     "qome", "yqomal", "yqumu", "qomo", "qWaqWame",
     "xeTe", "yxeTal", "xaxaTe",
     "fEze", "yfEzal", "yfiz", "yfafiz", "fafEze",
     "gWagWac", "tegWagWahu", "tensafefec", "'nsafefalehu",
     "tenkWakWa", "tenxeraxerk", "tekenawene", "tekWelaxto", "tekWelaxehu",
     "wexenegere", "'awexenegagere",
     "teZgWedegWede", "yZgWedegWedal", "teZgWedgWdo", "teZgWedgWed",
     "'aneTese", "'asneTese", "teneTese"]

OROMO = ["deebite", "deebi'e", "deebi'uu", "buqqaate", "buqqa'e", "buqqa'uu",
         "duute", "du'e", "du'uu", "beelofti", "beelawa",
         "dhagaya", "dhageenye", "dubbadhe", "dubbate",
         "dhaqxe", "argite", "agarte", "qabde",
         "gargaarra", "galla", "baase", "baafna",
         # 2p, 3p, interrogative, continuative, contemporaneous
         "beeloftan", "beeloftanii", "du'an", "du'ani", "du'anii",
         # Dative
         "galeef", "gallaaf", "galtaniif",
         # Noun forms
         "deemuu", "deemuun", "deemuudhaaf", "deemuunin",
         "deemaa", "deemaan", "deemaatti",
         # Perfect
         "qabeera", "qabdeerti", "qabneerra",
         # Irregular
         "jedhani", "jetteerta", "gochuf", "godhe", "godhaa", "godhii"]

ESPAÑOL = [## regular verbs
           # -ar
           'canto', 'cantas', 'canta', 'cantamos', 'cantan',
           'canté', 'cantaste', 'cantó', 'cantaron',
           'cantaba', 'cantabas', 'cantábamos', 'cantaban',
           'cantaré', 'cantarás', 'cantará', 'cantaremos', 'cantarán',
           'cante', 'cantes', 'cantemos', 'canten',
           'cantara', 'cantaras', 'cantáramos', 'cantaran',
           'cantaría', 'cantarías', 'cantaríamos', 'cantarían',
           'cánteles', 'cantémosles', 'cántenles', 'cántales',
           'cantar', 'cantarles', 'cantando', 'cantándoles',
           # -er
           'como', 'comes', 'come', 'comemos', 'comen',
           'comí', 'comiste', 'comió', 'comimos', 'comieron',
           'comía', 'comías', 'comíamos', 'comían',
           'comeré', 'comerás', 'comerá', 'comeremos', 'comerán',
           'coma', 'comas', 'comamos', 'coman',
           'comiera', 'comieras', 'comiéramos', 'comieran',
           'comería', 'comerías', 'comeríamos', 'comerían',
           'cómalo', 'cómanlo', 'comámoslo', 'cómelo',
           'comer', 'comerlo', 'comiendo', 'comiéndomelo',
           # phonological/orthographic changes
           'quiero', 'queremos', 'quiera', 'quieran',
           'juego', 'juegas', 'jugamos', 'juegue', 'jueguen',
           'pido', 'pides', 'pedimos', 'pidieron', 'pidiera', 'pidas',
           'divierto', 'divirtiendo', 'divertimos',
           'elijo', 'eliges', 'elegimos', 'eligieron',
           'cazo', 'cazamos', 'cace', 'cacemos',
           'empiezo', 'empezamos', 'empiece', 'empiecen',
           'conozco', 'conozcan', 'conózcalas', 'conoces', 'conócelas',
           'envío', 'cambio', 'envió', 'cambié', 'cámbielo', 'cámbialo',
           # irregular
           'traduzco', 'traduces', 'traducimos', 'traduje', 'tradujéramos',
           'traigo', 'salgo', 'oigo', 'huele', 'caigan', 'tráigala', 'tráemelas',
           'hemos', 'voy', 'soy', 'es', 'somos', 'doy', 'estoy', 'estás',
           'pude', 'traje', 'hice', 'deshice', 'fui', 'di', 'dímelo',
           'dirijo', 'puso', 'cupo', 'fue', 'dio', 'quiso',
           'dijeron', 'pusieron', 'oyeron', 
           'saldremos', 'sabrás', 'harán', 'querría', 'valdríamos'
           # clitic pronouns
#           'te miré', 'se lo digo', 'me las encantan', 'se vistieron'
           ]

class MorphoTC(unittest.TestCase):
    '''Superclass for all test cases.'''

    def get_fsts(self, abbrev, pos, phon=False, segment=False, verbose=False):
        """Get the POSMorphology object for a language and part-of-speech category."""
        l3.load_lang(abbrev, segment=segment, phon=phon, load_morph=True, verbose=verbose)
        lang = l3.morpho.get_language(abbrev, phon=phon, segment=segment, load=True,
                                      verbose=verbose)
        if lang:
            return lang.morphology[pos]

class AnalTC(MorphoTC):
    """Test case for analysis of words in a given language.
    Just tests whether there is an analysis, not whether it's right."""

    def anal_test(self, language, pos, words, segment=False):
        fsts = self.get_fsts(language, pos, segment=segment)
        for word in words:
            print('Analyzing', word)
            anal = fsts.anal(word, segment=segment)
            self.assertGreater(len(anal), 0, "{} can't be analyzed".format(word))

    def test_am_tam(self):
        self.anal_test('am', 'v', AMH_TAM)
    
    def test_am(self):
        self.anal_test('am', 'v', AMHARIC, segment=False)

    def test_am_seg(self):
        self.anal_test('am', 'v', AMHARIC, segment=True)

    def test_am_seg_tam(self):
        self.anal_test('am', 'v', AMH_TAM, segment=True)        

    def test_om_v(self):
        self.anal_test('om', 'v', OROMO)

    def test_es_v(self):
        self.anal_test('es', 'v', ESPAÑOL)

    def test_gn(self):
        self.anal_test('gn', 'v', GUARANI)

def main():
    pass

if __name__ == "__main__": main()
