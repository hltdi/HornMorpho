"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2019. PLoGS and Michael Gasser <gasser@indiana.edu>.

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

Multilingual objects and morphological translation.
"""

import yaml
from .languages import *

class Biling():
    """An object storing FSTs and a bilingual root dictionary for a language pair."""

    def __init__(self, source, target,
                 load_lexicon=False, load_data=True):
        """source and target are language abbreviations."""
        self.source = get_language(source)
        self.target = get_language(target)
        self.src_abbrev = self.source.abbrev
        self.targ_abbrev = self.target.abbrev
        self.name = "{}=>{}".format(self.src_abbrev, self.targ_abbrev)
#        self.directory = self.get_dir()
#        name = []
#        for l, ps in self.items():
#            name.append(l + ':' + '[' + ','.join([p.pos for p in ps]) + ']')
#        self.name = '<<' + ' | '.join(name) + '>>'
        self.lexicon = {}
        self.data = {}
        if load_lexicon:
            self.read_lexicon()
        if load_data:
            self.read_data()

    def __repr__(self):
        return self.name

    def get_dir(self):
        """Where data for this Biling is kept."""
        return self.source.get_trans_dir()

    def get_data_file(self):
        path = os.path.join(self.get_dir(), self.targ_abbrev + ".dt")
        return path

    def get_lex_file(self):
        path = os.path.join(self.get_dir(), self.targ_abbrev + ".lex")
        return path

    def read_data(self, expand=True):
        """Read translation data from .dt file."""
        print("Reading data for {}".format(self))
        dct = yaml.load(open(self.get_data_file(), encoding='utf8'), Loader=yaml.FullLoader)
        if expand:
            for pos, props in dct.items():
                for key, values in props.items():
                    if key == 'featmaps':
                        for cat, feats in values.items():
                            for index, sffeats in enumerate(feats):
                                sffeats = [(FeatStruct(f) if isinstance(f, str) and '[' in f else f) for f in sffeats]
#                                if isinstance(source, str) and '[' in source:
#                                    source = FeatStruct(source)
#                                # otherwise 'source' is a simple string or boolean
#                                target = FeatStruct(target)
#                            print("source: {}, target: {}".format(source_fs.__repr__(), target_fs.__repr__()))
                                feats[index] = sffeats
#                                (source, target)
        self.data = dct

    def adapt_features(self, pos, features):
        """Convert source features to target features."""
        featmap = self.data[pos]['featmaps']
        tfeatvalues = FeatStruct(freeze=False)
        for cat, feats in featmap.items():
            svalues = features.get(cat, 'missing')
            print("Adapting {}, value {}".format(cat, svalues.__repr__()))
            if svalues != 'missing':
                for f in feats:
                    sfeats2 = ''
                    sfeats = f[0]
                    tfeats = f[-1]
                    if len(feats) == 3:
                        sfeats2 = f[1]
#                for sfeats, tfeats in feats:
                    print("Trying {} ({}) => {}".format(sfeats.__repr__(), sfeats2.__repr__(), tfeats.__repr__()))
                    u = simple_unify(svalues, sfeats)
                    if u != 'fail':
                        if not sfeats2 or simple_unify(features, sfeats2) != 'fail':
                            print("  {} unifies with {} ({})".format(features.__repr__(), sfeats.__repr__(), sfeats2.__repr__()))
                            tfeatvalues.update(tfeats)
                            break
                
        return tfeatvalues

    def analyze(self, form):
        """Analyze the source form, returning list of (root, feature_FS) pairs."""
        return self.source.anal_word(form, preproc=True)

    def generate(self, pos, root, feats, postproc=True):
        """Generate the target form, given POS, root, and features.
        If postproc, convert output to target orthography."""
        posmorph = self.target.morphology.get(pos)
        if not posmorph:
            print("Generation not possible for {}".format(pos))
            return
        return posmorph.gen(root, update_feats=feats, interact=False,
                            postproc=postproc)

    def read_lexicon(self):
        abbrev = source + target
        if abbrev in self.lexicons:
            return self.lexicons[abbrev]
        else:
            import yaml
            file = self.get_lex_file(source, target)
            lexicon = yaml.load(open(file, encoding='utf8'))
            self.lexicons[abbrev] = lexicon
            return lexicon

    def tra(self, morph=False, lexicon=False):
        """Make an interactive text menu for translating words or phrases."""
        first = True
        tdir = ''
        while True:
            t = '1'
            if not first:
                t = input("\n¿Traducir de nuevo?  [1]   |   ¿Terminar?   [2] >> ")
            if t == '2':
                return
            first = False
            tdir = self.tra1(morph=morph, lexicon=lexicon, tdir=tdir)

    def tra1(self, morph=False, lexicon=False, tdir=''):
        """Make an interactive text menu for translating words or phrases."""
        lex = True
        if morph:
            lex = False
        elif lexicon:
            lex = True
        else:
            transi = input("-Morfología          [1]   |   +Morfología  [2] >> ")
            if transi and transi == '2':
                lex = False
        if not tdir:
            dir1 = "{}->{}".format(self.langs2[0], self.langs2[1])
            dir2 = "{}->{}".format(self.langs2[1], self.langs2[0])
            direction = input("Dirección: {}    [1]   |   {}       [2] >> ".format(dir1, dir2))
            if direction and direction == '2':
                tdir = self.langs2[1] + self.langs2[0]
            else:
                tdir = self.langs2[0] + self.langs2[1]
        item = input("Palabra   o   frase   para   traducir           :: ")
        if lex:
            trans = self.tralex(item, direction=tdir)
            if not trans:
                print("   Traducción no encontrada")
        else:
            trans = self.tramorf(item, direction=tdir)
            if not trans:
                print("   Traducción no encontrada")
        return tdir

    def tramorf(self, phrase, fsts=None, direction='', verbose=False):
        """Use lexicons and morphological FSTs to attempt to translate phrase."""
        # phrase must be a list of words
        if isinstance(phrase, str):
            phrase = phrase.split()
        if not fsts:
            fsts = self.fsts.get(direction)
        if not fsts:
            if verbose:
                print("No FSTs found")
                return []
        for f in fsts:
            if verbose:
                print("Attempting to translate with FST {}".format(f))
            trans = f.transduce(phrase, verbose=verbose)
            if trans:
                return trans
        return []

    def tralex(self, item, direction='', root=None, only_one=False):
        """Use lexicons to attempt to translate item."""
        dct = self.lexicons.get(direction)
        if not dct:
            print('No lexicon loaded')
            return []
        key = root if root else item
        entries = dct.get(key)
        if not entries:
            return []
        res = []
        for sphrase, troot, tphrase, tpos in entries:
            if sphrase == item:
                if only_one:
                    print('   {}'.format(tphrase))
                    return [tphrase]
                else:
                    print('   {}'.format(tphrase))
                    res.append(tphrase)
        return res

    @staticmethod
    def get_translations(source, lexicon, tlang, one_word=True, one=False, match_all=True):
        """
        Get translations for source root in lexicon dict.
        """
        targets = lexicon.get(source, [])
        res = []
        for sphrase, target, tphrase, tpos in targets:
            if match_all and source != sphrase:
                continue
            if ' ' in tphrase and one_word:
                continue
            res.append((target, tpos))
            if one and len(res) == 1:
                return res
        return res

    @staticmethod
    def gen_target(root, feats, pos, prefixes=None, final=False, verbose=False):
        if verbose:
            print('Generating {}: {}'.format(root, feats.__repr__()))
#        result = pos.gen(root, interact=False, update_feats=feats)
        result = pos.generate(root, feats, interact=False, print_word=final)
        return [r[0] for r in result]

    @staticmethod
    def match_cond(root, feats, condFS):
        if condFS:
            if not Multiling.match_feats(feats, condFS):
                return False
        return True

    @staticmethod
    def match_feats(fs1, fs2):
        """Match two FSSetss, converting strings to FSSets if necessary."""
        if not isinstance(fs1, FSSet):
            fs1 = FSSet(fs1)
        if not isinstance(fs2, FSSet):
            fs2 = FSSet(fs2)
        return fs1.unify(fs2)

class TraFST:
    """FST for phrase translation.
    """

    stateID = 0

    def __init__(self, multiling, slang, tlang, states=None):
        self.multiling = multiling
        # Language abbreviations
        self.slang = slang
        self.tlang = tlang
        self.states = states if states else {}
        self.lexicon = multiling.get_lexicon(slang, tlang)
        # Initial state ID
        self.init = -1
        # Add the FST to the appropriate list in the multiling
        abbrev = slang + tlang
        if abbrev in multiling.fsts:
            multiling.fsts[abbrev].append(self)
        else:
            multiling.fsts[abbrev] = [self]

    def add_state(self, ins=None, outs=None):
        ins = ins if ins else []
        outs = outs if outs else []
        id = TraFST.stateID
        if not self.states:
            self.init = id
        self.states[id] = [ins, outs]
        TraFST.stateID += 1
        return id

    def add_arc(self, source, dest, arc):
        if source != None:
            # outs for source
            self.states[source][1].append(arc)
        if dest != None:
            # ins for dest
            self.states[dest][0].append(arc)
        arc.sstate = source
        arc.dstate = dest

    def make_arc(self, scond, tcond, fscond, name=''):
        return TraArc(scond, tcond, fscond, name=name)

    def is_final(self, state):
        return not self.states[state][1]

    def is_initial(self, state):
        return not self.states[state][0]

    def out_arcs(self, state):
        return self.states[state][1]

    def transduce(self, words, initial=None, one=False, verbose=False):
        init_tra_state = initial if initial else self.init_tra_state(words)
        init_fst_state = init_tra_state.fst_state
        init_arcs = self.out_arcs(init_fst_state)
        if not init_arcs:
            print('No out arcs from initial state!')
            return
        results = []
        stack = [(init_tra_state, init_arcs[0])]
        for arc in init_arcs[1:]:
            tra_state = init_tra_state.clone()
            stack.append((tra_state, arc))
        while stack:
            if verbose:
                print('Current stack: {}'.format(stack))
            tra_state, arc = stack.pop()
            if verbose:
                print('Current state {}, current arc {}'.format(tra_state, arc))
                print(' Current FS {}'.format(tra_state.fs.__repr__()))
            traverse = tra_state.traverse(arc, verbose=verbose)
            if traverse:
                if verbose:
                    print('Succeeded on arc {}'.format(arc))
                # Find the arcs out of the dest state
                new_fst_state = tra_state.fst_state
                if self.is_final(new_fst_state):
                    if verbose:
                        print('{} is a final state'.format(new_fst_state))
                    if tra_state.is_empty():
                        output = [' '.join(o) for o in tra_state.output]
                        for o in output:
                            print("--> {}".format(o))
#                        print('Output: {}'.format(output))
                        results.extend(output)
                    elif verbose:
                        print('But {} is not empty'.format(new_fst_state))
                else:
                    new_arcs = self.out_arcs(new_fst_state)
                    stack.append((tra_state, new_arcs[0]))
                    for arc in new_arcs[1:]:
                        new_tra_state = tra_state.clone()
                        stack.append((new_tra_state, arc))
            elif verbose:
                print('Failed on arc {}'.format(arc))
        return results                  

    def init_tra_state(self, words):
        sPOSs = self.multiling.get(self.slang)
        tPOSs = self.multiling.get(self.tlang)
        lexicon = self.lexicon
        return TraState(words, [], FeatStruct(), sPOSs, tPOSs,
                        lexicon, self.slang, self.tlang, self,
                        fst_state=self.init)

class TraState:
    """
    State of translation FST transduction:
    0 current word: [word, {POS: analysis, ...}]
    1 source words left
    2 current output
    3 current FeatStruct
    """

    id = 0

    def __init__(self, swords, output, fs,
                 sPOSs, tPOSs, s2tlex,
                 slang, tlang, fst,
                 sword=None, fst_state=-1, name=None):
        if not sword:
            self.sword = [swords[0], {}]
            self.swords = swords[1:]
        else:
            self.sword = sword
            self.swords = swords
        self.output = output
        self.fs = fs
        self.sPOSs = sPOSs
        self.tPOSs = tPOSs
        self.s2tlex = s2tlex
        self.slang = slang
        self.tlang = tlang
        self.fst = fst
        self.fst_state = fst_state
        self.name = name or ' '.join(swords)
        self.id = TraState.id
        self.position = 0
        TraState.id += 1

    def __repr__(self):
        return '{{{{{}:#{}|{}}}}}'.format(self.name, self.id, self.sword[0])

    def clone(self):
        sword = copy.deepcopy(self.sword)
        swords = self.swords.copy()
        output = self.output.copy()
        fs = self.fs.copy(deep=True)
        return TraState(swords, output, fs,
                        self.sPOSs, self.tPOSs, self.s2tlex,
                        self.slang, self.slang, self.fst,
                        sword=sword, fst_state=self.fst_state, name=self.name)

    def is_empty(self):
        """Have all words been consumed?"""
        return not self.sword

    def traverse(self, arc, final=False, verbose=False):
        """
        Traverse a TraArc, updating the TraState, possibly generating
        new TraStates or returning False if traversal fails.
        """
        if verbose:
            print('**{} traversing {}'.format(self, arc))
        # Test source condition, parsing source word if necessary.
        if not self.match_source(arc.scond, verbose=verbose):
            return False
        ## Update FS
        if not self.update_fs(arc.fscond, verbose=verbose):
            return False
        ## Update target
        if not self.update_target(arc.tcond, final=final, verbose=verbose):
            return False
        ## Update source words
        if 'pop' in arc.scond:
            self.update_words(verbose=verbose)
        self.fst_state = arc.dstate
        return True

    def get_target_pos(self, abbrev):
        for p in self.tPOSs:
            if p.pos == abbrev:
                return p

    def get_word_fvs(self, feat, POSs):
        """List values for feat string in analyses of current word for pos."""
#        print('Getting word FVs {}, {}'.format(feat, pos))
        anals = []
        for pos in POSs:
            if pos in self.sword[1]:
                anals.extend(self.sword[1].get(pos))
#        print('Found anals {}'.format(anals))
        if anals:
            # only the first anal
            return [a.get(feat) for a in anals[0][1]]
        return []
    
    def copy_fs(self, feat, POSs, verbose=False):
        """Copy value(s) of feat in analyses of current word for pos to current FS."""
        fvs = self.get_word_fvs(feat, POSs)
        if verbose:
            print('Copying {} to FS'.format(fvs))
        if fvs:
            # For now just copy the first feature value
            self.fs.update({feat: fvs[0]})
#            print('FS now {}'.format(self.fs.__repr__()))

    def match_source(self, cond, verbose=False):
        """Match the source condition on an arc."""
        if verbose:
            print('*Matching source')
        if not cond:
            # Don't update swords and sword.
            return True
        if self.is_empty():
            # Everything else requires a current word.
            return False
        word = self.sword[0]
        condanal = cond.get('anal')
        condFS = condroot = condposs = None
        if condanal:
            condroot, condposs, condFS = condanal
        if condFS or condroot:
            # word analysis dict
            analyses = self.sword[1]
            if not isinstance(condFS, FSSet):
                condFS = FSSet(condFS)
            anals = []
            # We have to analyze the input word
            if verbose:
                print("Looking for anals in {}".format(self.sPOSs))
            for pos in self.sPOSs:
                pos_abbrev = pos.pos
                if pos_abbrev in condposs:
                    if pos_abbrev in analyses:
                        if verbose:
                            print("There are already analyses {}".format(analyses[pos_abbrev]))
                        # There are already analyses of the word
                        anals.extend(analyses[pos_abbrev])
                    else:
                        if verbose:
                            print("Analyzing {} with FS {} in {}".format(word, condFS.__repr__(), pos))
                        anal = pos.analyze(word, init_weight=condFS)  #, trace=1)
                        if anal:
                            if not condroot or all([(condroot == a[0]) for a in anal]):
                                analyses[pos_abbrev] = anal
                                anals.extend(anal)
#            if verbose:
#                print('Found anals', anals)
            # There may be multiple analyses
            if not anals:
                if verbose:
                    print("No analyses found")
                return False
            else:
                if len(anals) > 1:
                    print('Análisis multiples encontrados')
                # Check only the first analysis
                root, feats = anals[0]
                if not Multiling.match_cond(root, feats, condFS):
#                    if verbose:
#                        print('Updating words')
#                    self.update_words()
#                    return True
#                else:
                    if verbose:
                        print('Analysis fails to match source condition')
                    return False
        else:
            # No analysis required for matching; just match the raw word
            condword = cond.get('word')
            if condword and word != condword:
                if verbose:
                    print('Word fails to match source condition')
                return False
            else:
                return True
        return True

    def update_fs(self, cond, verbose=False):
        if verbose:
            print('*Updating FS')
        if cond:
            add = cond.get('add')
            if add:
                if not isinstance(add, FeatStruct):
                    add = FeatStruct(add)
                new_fs = simple_unify(self.fs, add)
                if new_fs == 'fail':
                    if verbose:
                        print('Update FS fails to unify')
                    return False
                self.fs = new_fs
            copy = cond.get('copy')
            if copy:
                feats, POSs = copy
                if not isinstance(POSs, list):
                    POSs = [POSs]
                for f in feats:
                    self.copy_fs(f, POSs, verbose=verbose)
        return True

#    def update_fs(self, update):
#        """Update the current FS, unifying it with FS update."""
#        if not isinstance(update, FeatStruct):
#            update = FeatStruct(update)
#        new_fs = simple_unify(self.fs, update)
#        if new_fs == 'fail':
#            return False
#        self.fs = new_fs
#        return True

    def update_words(self, verbose=False):
        if verbose:
            print('*Popping words')
        self.position += 1
        if self.swords:
            self.sword = [self.swords[0], {}]
            self.swords.pop(0)
        else:
            self.sword = []

    def update_target(self, cond, final=False, verbose=False):
        if verbose:
            print("*Updating target")
        if not cond:
            return True
        if 'gen' in cond:
            troot, tfs, sPOSs = cond['gen']
            if troot == '?t':
                if not isinstance(sPOSs, list):
                    sPOSs = [sPOSs]
                # Use the translation of sroot
                # find sroot and sanal
                anals = []
                for spos in sPOSs:
                    if spos in self.sword[1]:
                        anals.extend(self.sword[1][spos])
                if not anals:
                    if verbose:
                        print("No analyses found for {}".format(sPOSs))
                # Just get one analysis
                sroot, sanal = anals[0] # self.sword[1][spos][0]
                trans = Multiling.get_translations(sroot, self.s2tlex, self.tlang,
                                                   one_word=True, one=False, match_all=True)
                if not trans:
                    if verbose:
                        print('No translations for sroot {}'.format(sroot))
                    return False
                fs = self.fs
                if tfs:
                    # Should be a list of FeatStructs (or maybe a FSSet)
                    # Incorporate features in each
                    u_fs = []
                    for f in tfs:
                        if not isinstance(f, FeatStruct):
                            f = FeatStruct(f)
#                            print('Unifying state FS {} with arc gen FS {}'.format(fs.__repr__(), f.__repr__()))
                            u = simple_unify(fs, f)
                            if u == 'fail':
                                if verbose:
                                    print('Current FS failed to unify target condition')
                                return False
                            u_fs.append(u)
                    # Make a dict of POS FSTs: updated FSs for generation
                    pos_dct = {}
                    for t in trans:
                        pos_abbrev = t[1]
                        if pos_abbrev in pos_dct:
                            # Already recorded
                            continue
                        pos = self.get_target_pos(pos_abbrev)
                        # Combine the features in tfs with the default
                        pos_u_fs = [pos.update_FS(pos.defaultFS, t) for t in u_fs]
                        pos_dct[pos_abbrev] = pos_u_fs

                    new_out = []

                    for t in trans:
                        root = t[0]
                        pos_abbrev = t[1]
                        pos = self.get_target_pos(pos_abbrev)
                        features = pos_dct[pos_abbrev]
                        for f in features:
                            if not f:
                                continue
                            gen = Multiling.gen_target(root, f, pos, final=final, verbose=verbose)
                            for g in gen:
                                if self.output:
                                    for o in self.output:
                                        out = o + [g]
                                        new_out.append(out)
#                                        if final:
#                                            print(new_out)
                                else:
                                    new_out.append([g])
#                                    if final:
#                                        print(g)
                    if not new_out:
                        if verbose:
                            print('Generation failed')
                        return False
                    self.output = new_out
            elif sPOSs:
                # If there's a POSs, then generate the word with the given root
                # but treat this as a *target* POS
                pos = self.get_target_pos(sPOSs)
                fs = self.fs
                if tfs:
                    # Should be a list of FeatStructs (or maybe a FSSet)
                    # Incorporate features in each
                    u_fs = []
                    for f in tfs:
                        if not isinstance(f, FeatStruct):
                            f = FeatStruct(f)
#                            print('Unifying state FS {} with arc gen FS {}'.format(fs.__repr__(), f.__repr__()))
                            u = simple_unify(fs, f)
                            if u == 'fail':
                                if verbose:
                                    print('Current FS failed to unify target condition')
                                return False
                            u_fs.append(u)
                    # Combine the features in tfs with the default
                    pos_u_fs = [pos.update_FS(pos.defaultFS, t) for t in u_fs]
                    new_out = []
                    for f in pos_u_fs:
                        if not f:
                            continue
                        gen = Multiling.gen_target(troot, f, pos, final=final, verbose=verbose)
                        for g in gen:
                            if self.output:
                                for o in self.output:
                                    out = o + [g]
                                    new_out.append(out)
                            else:
                                new_out.append([g])
                    if not new_out:
                        if verbose:
                            print('Generation failed')
                        return False
                    self.output = new_out
            else:
                if self.output:
                    for i, o in enumerate(self.output):
                        self.output[i] = o + [troot]
                else:
                    self.output = [[troot]]
        return True

class TraArc:
    """
    Arc in a translation FST:
    1 input (source) condition
      a dict: {'word': string, 'root': string, 'feats': [POSs, FS]}
    2 output (target) condition
      a dict: {'words': string, 'gen': [POSs, ??]}
    3 FS update condition
      a dict: {'add': FS, 'copy': [FS feats]}
    """

    arcID = 0

    def __init__(self, scond, tcond, fscond, name='', sstate=-1, dstate=-1):
        self.scond = scond
        self.tcond = tcond
        self.fscond = fscond
        self.sstate = sstate
        self.dstate = dstate
        self.set_name(name)

    def __repr__(self):
        return '>>{}<<'.format(self.name)
# [[{} {} {}]]'.format(self.scond, self.tcond, self.fscond)

    def set_name(self, name):
        if name:
            self.name = name
        else:
            self.name = str(TraArc.arcID)
            TraArc.arcID += 1

##    def graphics(self):
##        start_graphics(self.values())

#    def load_fst(self):
#        for pos in self.values():
#            pos.load_fst()

##    def set_transfer_fs(self, fss):
##        '''Set the transfer FSs.'''
##        self.transfer_fss = fss
##
##    def transfer1(self, source, source_fs, target):
##        source_trans = FeatStruct()
##        source_trans[source] = source_fs
##        target_morphpos = self[target]
##        for fs in self.transfer_fss:
##            unify_fs = unify(source_trans, fs)
##            if unify_fs:
##                target_morphpos.assign_defaults(unify_fs[target])
##                return unify_fs
##
##    def transfer(self, source_lang, source_fss, target_lang):
##        """Root, FS pairs for generating target word(s)."""
##        target = []
##        for fs_set in source_fss:
##            for fs in fs_set:
##                target_fs = self.transfer1(source_lang, fs, target_lang)
##                if target_fs:
##                    # The source FS unifies with some transfer FS
##                    if target_lang in target_fs:
##                        target_glosses = target_fs[target_lang]['g'], split[',']
##                        for gloss in target_gloses:
##                            target.append((gloss, target_fs))
##        return target
                    
