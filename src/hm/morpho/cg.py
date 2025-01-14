'''
Constraint grammar for HornMorpho.
'''

import subprocess
import re
import os
from .utils import first, YES
from .usr import *
#from subprocess import Popen, PIPE, run
# import sys

USER_DIR = os.path.join(os.path.dirname(__file__), 'usr')

#CG3 = '/usr/local/bin/vislcg3'

class CG:

    para_delim = "<¶>"

    wordform_re = re.compile(r'\"\<(.+)\>\"')

    cg_path = ''

    YNprompt = "[y/n] >>> "

    def __init__(self, language, disambig=True):
        self.language = language
        # There are two kinds of rules: "disambiguation" and "annotation" ("dependencies")
        self.disambig = disambig
        self.initialized = False
        self.init_CG()
#        self.cg_path = CG3
#        self.disambig_path = language.get_disambig_file()
#        self.dep_path = language.get_dep_file()
        self.rules_path = language.get_disambig_file() if disambig else language.get_dep_file()

    def __repr__(self):
        return "CG:{}:{}".format('disamb' if self.disambig else 'dep', self.language.abbrev)

    def rule_type(self):
        return 'disambiguation' if self.disambig else 'annotation'

    @staticmethod
    def set_CG_path(path, write=True):
        while True:
            if file_exists(path):
                CG.cg_path = path
                print("Setting CG3 path to {}".format(path))
                if write:
                    write_path('CG3', path)
                return True
            else:
                print("File at {} does not exist; try another?".format(path))
                another = input(CG.YNprompt)
                if another in YES:
                    print("What's the path?")
                    path = input(CG.YNprompt)
                else:
                    print("No path to a file provided")
                    return False

    def init_CG(self):
        '''
        Find the path to CG3 or set it or ignore CG3.
        '''
        def installed2path():
            done = False
            while not done:
                print("Enter the path where VISL CG3 is installed (probably something like '/usr/local/bin/vislcg3')")
                if path := input(">>> "):
                    if CG.set_CG_path(path):
                        self.initialized = True
                        done = True
                    else:
                        return
                else:
                    print("You didn't enter a path; would you like to ignore CG3 {} for now?".format(self.rule_type))
                    ignore = input(CG.YNprompt)
                    if ignore in YES:
                        return
        if CG.cg_path:
            self.initialized = True
            return
        if path := get_path('CG3'):
            if CG.set_CG_path(path, write=False):
                self.initialized = True
                return
            else:
                return
        print("I can't find the path for VISL CG3")
        loaded = input("To use the disambiguation and annotation rules, you have to have installed VISL CG3. Have you?\n{}".format(CG.YNprompt))
        if loaded in YES:
            installed2path()
        else:
            print("Would you like to install VISL CG3?")
            install = input(CG.YNprompt)
            if install in YES:
                print("Instructions for installation are here: https://edu.visl.dk/cg3/chunked/installation.html")
                print("Have you successfully installed the program?")
                installed = input(CG.YNprompt)
                if installed in YES:
                    installed2path()
                else:
                    print("Would you like to ignore CG3 {} for now?".format(self.rule_type()))
                    ignore = input(CG.YNprompt)
                    if ignore in YES:
                        return
            else:
                print("Continuing without {} rules...".format(self.rule_type()))
                return

    @staticmethod
    def open_sentence_file(path):
        return subprocess.Popen(['cat', path], stdout=PIPE)

    @staticmethod
    def anal2reading(analysis, verbosity=0):
        '''
        Convert a HM analysis (one element in a Word list) to a Reading object.
        '''
        feats = analysis.get('pos', '')
        um = analysis.get('um', '')
        if um:
            um = ' '.join([u.replace('*', '') for u in um.split(';')])
            feats = "{} {}".format(feats, um)
        lemma = analysis.get('lemma', analysis.get('token'))
        string = '"{}" {}'.format(lemma, feats)
        return Reading(string)

    @staticmethod
    def word2cohort(word, verbosity=0):
#        if verbosity:
#            print("  Converting {} to cohort".format(word))
        token = word.name
        result = ['"<{}>"'.format(token)]
        if not word.readings:
            readings = [CG.anal2reading(analysis, verbosity=verbosity) for analysis in word]
#            if not self.disambig and len(readings) > 1:
#                print("Warning: {} has more than one analysis!".format(word))
            word.readings = readings
        result.extend(['\t' + r.string for r in word.readings])
        return Cohort(token, word.readings)

    @staticmethod
    def sentence2cohorts(sentence, predelim='', postdelim='', write2='', verbosity=0):
        '''
        Convert an HM Sentence object to a list of Cohort objects.
        '''
#        if verbosity:
#            print("Converting {} to CG".format(sentence))
        cohorts = []
        if predelim:
            cohorts.append(Cohort(predelim, []))
        for word in sentence.words:
            cohorts.append(CG.word2cohort(word, verbosity=verbosity))
        if postdelim:
            cohorts.append(Cohort(postdelim, []))
        return CGSentence(cohorts)
#        if write2:
#            with open(write2, 'w', encoding='utf8') as file:
#                print(result, file=file)

    @staticmethod
    def sentstring2CGsent(sentstring):
        '''
        Convert a sentence CG string to a CGSentence.
        '''
        s = sentstring.split("\n")
        wf = ''
        cohorts = []
        Readings = []
        for line in s:
            if not line.strip():
                continue
            match = CG.wordform_re.match(line)
            if match:
                wordform = match.group(1)
                if wf:
                    cohorts.append((wf, Readings))
                    wf = ''
                    Readings = []
                # a new cohort
                wf = wordform
            elif line.startswith(';'):
                # a removed reading
                line = line[1:].strip()
                reading = Reading(line, removed=True)
                Readings.append(reading)
            elif 'SUBSTITUTE' in line:
                line = line[1:].strip()
                reading = Reading(line, substitution=True)
                Readings.append(reading)
            else:
                Readings.append(Reading(line.strip()))
        cohorts.append((wf, Readings))
        cohorts = [Cohort(w, r) for w, r in cohorts]
        cgsent = CGSentence(cohorts)
        return cgsent

    def call_cg3(self, sentences, trace=True, verbosity=0):
        '''
        Run the rules in self.rules_path on the sentences in sentences,
        a path or a stream.
        Return the result as a string with deleted readings marked by ; (disambiguation)
        or tags added for ID, dependencies, and relations (annotation).
        '''
        if verbosity:
            print("  Running rules at {}".format(self.rules_path))
        args = [CG.cg_path, '-g', self.rules_path]
        if trace:
            args.append('-t')
        result = subprocess.run(args, input=sentences, capture_output=True, text=True)
        return result.stdout.strip()

    def realize_rules(self, sentence, sentstring, verbosity=0):
        '''
        sentstring is the output of rules applied to sentence.
        Realize the rules by
           disambiguation: removing any readings that have been marked as removed.
           annotation: saving any relations and dependencies in the Sentence object.
        '''
        if verbosity:
            if self.disambig:
                print("  Disambiguating {}".format(sentence.words))
            else:
                print("  Annotating {}".format(sentence.words))
        todel = {}
        CGsent = CG.sentstring2CGsent(sentstring)
#        if verbosity:
#            print("CGsent {}".format(CGsent.format()))
        if len(sentence.words) != len(CGsent.cohorts):
            print("Something wrong: # words {} != # cohorts {}".format(len(sentence.words), len(CGsent.cohorts)))
            return
        if not self.disambig:
            root, relations = CGsent.get_relations(verbosity=verbosity)
            if root >= 0:
                if verbosity:
                    print("  Setting sentence root to word {}".format(root))
                sentence.root = root
            if relations:
                if verbosity:
                    print("  Setting sentence relations to {}".format(relations))
                sentence.relations = relations
            return root, relations
        for index, (word, cohort) in enumerate(zip(sentence.words, CGsent.cohorts)):
            td = self.realize_rules_word(word, cohort, verbosity=verbosity)
            if td:
                todel[index] = td
        return todel

    def realize_rules_word(self, word, cohort, verbosity=0):
        '''
        Realize the output of rules, given in Cohort instance cohort, to Word instance word.
        '''
        readings = cohort.readings
        if verbosity:
            print("  Disambiguating {} / {}".format(word, cohort))
        if len(word) != len(readings):
            print("  Something wrong with {}: # analyses {} != # reading {}".format(word, len(word), len(readings)))
            return
        todel = []
        substitutions = []
        for reading in readings:
            if reading.removed:
                found = False
                for index, r in enumerate(word.readings):
                    if reading.match(r):
                        todel.append(index)
                        found = True
                        break
                if not found:
                    print("REMOVED READING {} FOR {} NOT FOUND!".format(rd, word))
            elif reading.substitution:
                if verbosity:
                    print("    Substitution for {}".format(reading))
                found = False
                for index, r in enumerate(word.readings):
                    if reading.match(r):
                        if r.get_pos() != reading.get_pos():
                            # This is a POS substitution
                            substitutions.append((index, reading.get_pos()))
                            
        if todel:
            word.remove(todel)
            if verbosity:
                print("  Removed reading(s) {} from {}".format(todel, word))
        if substitutions:
            for index, pos in substitutions:
                if verbosity:
                    print("  Changing POS for reading {} in {} to {}".format(index, word, pos))
                word.change(index, pos=pos)
        return todel

    def run(self, sentence, predelim='', postdelim='', write2='', verbosity=0):
        '''
        Run rules on sentence and apply the changes or updates.
        If disambiguation, possibly delete readings of some cohorts (words).
        If annotation, possibly set the sentence root and relations.
        '''
#        if verbosity:
        print("Running {} rules".format(self.rule_type()))
        cgsent = CG.sentence2cohorts(sentence, predelim=predelim, postdelim=postdelim, verbosity=verbosity)
        rule_out = self.call_cg3(cgsent.format(), trace=True, verbosity=verbosity)
        if not rule_out:
            print("  Rules returned nothing!")
            return
        return self.realize_rules(sentence, rule_out, verbosity=verbosity)

class Cohort:
    '''
    A CG cohort: a word with one or more readings.
    '''

    def __init__(self, word, readings):
        self.word = word
        self.readings = readings

    def __repr__(self, short=False):
        if short:
            return "{}:[{}]".format(self.word, len(self.readings))
        return ">> {} : {} <<".format(self.word, self.readings)

    def format(self):
        return '"<{}>"\n{}'.format(self.word, '\n'.join([r.format() for r in self.readings]))

    @staticmethod
    def format_wordform(wf):
        return '"<{}>"'.format(wf)

    def get_id_tag(self):
        return self.readings[0].get_id_tag()

    def get_rel_tags(self):
        return self.readings[0].get_rel_tags()

    def get_dep_tags(self):
        return self.readings[0].get_dep_tags()

    def get_id(self):
        return self.readings[0].get_id()

    def get_rels(self):
        return self.readings[0].get_rels()

    def get_deps(self):
        return self.readings[0].get_deps()

class Reading:
    '''
    A CG reading: a string containing a form, a POS, and, optionally a list of features and one or more
    tags inserted by rules.
    '''

    POS_match = {'SCONJ': ['ADPCONJ']}

    def __init__(self, string, removed=False, substitution=False):
        self.string = string
        self.items = string.split()
        self.removed = removed
        self.substitution = substitution

    def __repr__(self):
        return ">{} {} <".format(';;' if self.removed else '', self.string)

    def format(self):
        return "\t{}".format(self.string)

    def get_lemma(self):
        return self.items[0]

    def get_pos(self):
        return self.items[1]

    def get_features(self):
        '''
        Morphological features.
        Note: this means that features *cannot* contain :.
        '''
        return [x for x in self.items[2:] if ':' not in x]

    def get_tags(self):
        return [x for x in self.items[1:] if ':' in x or x[0] == '#']

    def get_substitution_tags(self):
        return [x for x in self.get_tags() if x.startswith("SUBST")]

    def get_dep_tags(self):
        '''
        Dependency tags indicate a dependency but no relation between two words/cohorts.
        '''
        return [x for x in self.get_tags() if x[0] == '#']

    def get_rel_tags(self):
        '''
        Relation tags indicate a relation (and dependencey) between two words/cohorts.
        '''
        return [x for x in self.get_tags() if x[0] == 'R']

    def get_id_tag(self):
        '''
        ID tags assign a number to the word.
        '''
        if id := first(lambda x: x.startswith('ID'), [x for x in self.get_tags()]):
            return id

    def get_id(self):
        if tag := self.get_id_tag():
            return int(tag.split(':')[-1])

    def get_rels(self):
        if tags := self.get_rel_tags():
            return [tag.partition(':')[-1] for tag in tags]

    def get_deps(self, drop_self=True):
        if tags := self.get_dep_tags():
            deps = [[int(d) for d in tag[1:].split('->')] for tag in tags]
            if drop_self:
                deps = [(x, y) for x, y in deps if x != y]
            return deps

    def get_analysis(self):
        '''
        Lemma, POS, and morphological features (everything by CG tags).
        '''
        return [x for x in self.items if ':' not in x]

    def match(self, reading):
        '''
        Does this reading match another reading?
        This assumes the order of the features is the same.
        '''
        if self.substitution:
            # Substitution
            # Lemma has to match and POSs have to overlap (or belong to set in ; later make it more stringent
            pos = self.get_pos()
            rpos = reading.get_pos()
            lemma = self.get_lemma()
            rlemma = reading.get_lemma()
            # %% Fix this later; POS_match dict is to handle cases where the selected POS isn't strictly within
            # the combined POS, for example, SCONJ and ADVCONJ
            return lemma == rlemma and (pos in rpos or rpos in Reading.POS_match.get(pos, ''))
#        self.get_lemma() == reading.get_lemma() and self.get_pos() in reading.get_pos()
        return self.get_analysis() == reading.get_analysis()

class CGSentence:

    def __init__(self, cohorts):
        self.cohorts = cohorts

    def __repr__(self):
        string = ' ; '.join([c.__repr__(True) for c in self.cohorts])
        return ">>> {} <<<".format(string)

    def format(self):
        string = '\n'.join([c.format() for c in self.cohorts])
        # Need to add \n at end to get rules to prevent extra character at the end
        return string + '\n'

    def get_relations(self, verbosity=0):
        '''
        Return the relations between words/cohorts in the CGSentence as child->parent dicts.
        '''
        # child_windex: (parent_windex relation)
        idrelations = {}
        # child_windex: parent_windex
        dependencies = {}
        # ID: windex
        ids = {}
        root = -1
        for windex, cohort in enumerate(self.cohorts):
            if not cohort.readings:
                print("*** {} in {} has not readings".format(cohort, self.cohorts))
            id = cohort.get_id()
            if id:
                ids[id] = windex
            if verbosity:
                print("  ID for {}".format(cohort, id))
            rels = cohort.get_rels()
            if rels:
                for rel in rels:
                    rlabel, _, cid = rel.rpartition(':')
                    cid = int(cid)
                    idrelations[cid] = (id, rlabel)
            deps = cohort.get_deps()
            if deps:
                for dep in deps:
                    child, parent = dep
                    dependencies[child] = parent
        # Convert IDs to windex
        relations = {}
        for cid, (pid, label) in idrelations.items():
            cindex = ids.get(cid, None)
            if cindex is None:
                print("No index for cohort id {}!".format(cid))
                return
            relations[cindex] = (ids.get(pid), label)
        for cindex, pindex in dependencies.items():
            # dependency indeces are 1-initial cohort indices
            cindex -= 1
            if pindex == 0:
                # root
                root = cindex
            else:
                pindex -= 1
                if cindex in relations:
                    print("There is already an explicit relation for {}: {}".format(cindex, relations[cindex]))
                    continue
                relations[cindex] = (pindex, None)
        if verbosity:
            print("Cohort relations {}, root {}".format(relations, root))
        return root, relations
