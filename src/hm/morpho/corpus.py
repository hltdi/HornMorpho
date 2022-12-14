"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2022.
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

Analyzing and displaying corpora of sentences.
"""
from .languages import *
from tkinter import *
from tkinter.ttk import *
from tkinter.font import *
import time

class Corpus():
    """
    List of tokenized sentences to be segmented and displayed.
    """

    ID = 0

    def __init__(self, data=None, path='', start=0, n_sents=0, name='', batch_name='',
                 local_cache=None):
        self.batch_name = batch_name
        if not data and path:
            self.data = []
            try:
                filein = open(path, 'r', encoding='utf-8')
                lines = filein.readlines()
                if start or n_sents:
                    lines = lines[start:start+n_sents]
                for line in lines:
                    self.data.append(line.strip())
            except IOError:
                print('No such file or path; try another one.')
        elif data:
            # Raw sentences
            self.data = data
        else:
            self.data = []
        # Sentence objects, with pre-CoNLL-U word representations
        self.sentences = []
        self.language = get_language('amh', phon=False, segment=True, experimental=True)
#        # CoNLL-U strings for data
#        self.conllu = []
        self.name = name or batch_name or self.create_name()
        # Cache for storing segmentations
        self.local_cache = local_cache if isinstance(local_cache, dict) else {}

    def __repr__(self):
        return "C_{}".format(self.name)

    def create_name(self):
        name = "{}".format(Corpus.ID)
        Corpus.ID += 1
        return name

    def disambiguate(self, skip_unambig=True, timeit=False, verbosity=0):
        '''
        Show the segmentations in the GUI so words with multiple
        segmentations can be disambiguated.
        '''
        if not self.sentences:
            # Segment all sentences before creating GUI.
            self.segment(timeit=timeit)
        self.root = SegRoot(self, title=self.__repr__())
        self.root.mainloop()

    def segment(self, timeit=False, verbosity=0):
        """
        Segment all the sentences in self.data.
        % Later have the option of segmenting only some??
        """
        print("Segmenting sentences in {}".format(self))
        sentid = 1
        time0 = time.time()
        for sentence in self.data:
            sentence_obj = \
              self.language.anal_sentence(sentence, batch_name=self.batch_name, sentid=sentid, local_cache=self.local_cache)
            self.sentences.append(sentence_obj)
            sentid += 1
        if timeit:
            return print("Took {} seconds to segment {} sentences.".format(round(time.time() - time0), len(self.data)))

    def conlluify(self, degeminate=False, verbosity=0):
        """
        Convert all of the sentence pre-CoNNL-U representations to CoNNL-U.
        """
        for sentence in self.sentences:
            sentence.words2conllu(update_indices=True, degeminate=degeminate)

    def segment1(self, text='', sentindex=None):
        """
        Segment one sentence.
        """
        text = text or self.data[sentindex] if sentindex < len(self.data) else None
        if text:
            language = get_language('amh', phon=False, segment=True, experimental=True)
            sentence = language.anal_sentence(text, local_cache=self.local_cache)
            if sentence:
                self.all_sentences[sentindex] = sentence
        if sentence:
            self.root.segmentations = sentence.words
        return sentence

class SegRoot(Tk):
    '''
    Main window for the disambiguation GUI.
    '''

    sentencewidth = 60

    def __init__(self, corpus=None, title=None): # parent, corpus=None, width=1000, height=300, title=None):
        Tk.__init__(self) #, parent) #, width=width, height=height)
#        parent.title(title if title else "Corpus")
        self.title(title if title else "Corpus")
        fontfamilies = families()
        geezfamily =  "Abyssinica SIL" if "Abyssinica SIL" in fontfamilies else "Noto Sans Ethiopic"
#        print("families {}".format(fontfamilies[150:300]))
        self.corpus = corpus
        self.all_word_positions = {}
        self.word_positions = []
        # Create int variables for sentence and word index (1-based)
        self.init_vars()
        sentindex = self.sentvar.get()-1
        # Find the sentence in the corpus
        self.sentence = corpus.data[sentindex] if corpus.data else ''
        self.segmentations = []
        self.set_word_positions()
        self.always_paint = True
        self.geez_big = Font(family=geezfamily, size=20)
        self.geez_normal = Font(family=geezfamily, size=18)
        self.roman_big = Font(family="Arial", size=20)
        self.init_sentence_text()
        self.wordid_entry = self.init_wordid_entry()
        self.sentid_entry = self.init_sentid_entry()
        self.quit_button = Button(self, text="Quit", command=self.quit)
        self.quit_button.grid(row=0, column=2)
        self.sent_text.grid(row=1, columnspan=3)
        self.sentenceobj = self.corpus.sentences[sentindex]
        self.segmentations = self.sentenceobj.words
#        self.corpus.sentences[sentindex].words
        self.canvas = SegCanvas(self, corpus) # width=width-25, height=height-25)
        self.scrollbar = Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scrollbar.grid(row=2, column=3, sticky='ns')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.hscrollbar = Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.hscrollbar.grid(row=3, columnspan=3, sticky='ew')
        self.canvas.configure(xscrollcommand=self.hscrollbar.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#        self.show_segmentations()

    def quit(self):
        '''
        Quit the GUI, destroying all widgets.
        '''
#        self.parent.destroy()
        self.destroy()

    def init_vars(self):
        '''
        Creating int variables for word and sentence indices.
        '''
        self.sentvar = IntVar()
        self.sentvar.set(1)
        self.wordvar = IntVar()
        self.wordvar.set(1)

    def init_sentid_entry(self):
        '''
        Create the sentence ID Entry and forward/backward Buttons.
        '''
        sentframe = Frame(self, width=25, height=100)
        slabel = Label(sentframe, text="Sentence ID")
        se = Entry(sentframe, width=4, textvariable=self.sentvar, justify=CENTER)
        down = Button(sentframe, text="<", command=self.decrease_sentid, width=2)
        up = Button(sentframe, text=">", command=self.increase_sentid, width=2)
        slabel.grid(row=0, columnspan=2)
        se.grid(row=1, columnspan=2)
        down.grid(row=2, column=0)
        up.grid(row=2, column=1)
        se.bind("<Return>", self.get_sentid)
        sentframe.grid(row=0, column=0, padx=10)
        return se

    def init_wordid_entry(self):
        '''
        Create the word ID Entry and forward/backward Buttons.
        '''
        wordframe = Frame(self, width=25, height=100)
        wlabel = Label(wordframe, text="Word ID")
        we = Entry(wordframe, width=4, textvariable=self.wordvar, justify=CENTER)
        down = Button(wordframe, text="<", command=self.decrease_wordid, width=2)
        up = Button(wordframe, text=">", command=self.increase_wordid, width=2)
        wlabel.grid(row=0, columnspan=2)
        we.grid(row=1, columnspan=2)
        down.grid(row=2, column=0)
        up.grid(row=2, column=1)
        we.bind("<Return>", self.get_wordid)
        wordframe.grid(row=0, column=1, padx=10)
        self.highlight_word(0)
        return we

    def get_sentid(self, event):
        '''
        Get the current sentence ID (1 greater than actual ID).
        '''
        new_id = int(self.sentid_entry.get())
        self.set_sentid(new_id)

    def set_sentid(self, new_id):
        '''
        Set the sentence ID and the corresponding sentence.
        '''
        if 1 <= new_id <= len(self.corpus.data):
            self.sentvar.set(new_id)
            self.sentence = self.corpus.data[new_id-1]
            self.set_sentence(new_id-1)

    def get_wordid(self, event):
        '''
        Get the current word ID (1 greater than actual ID).
        '''
        new_id = int(self.wordid_entry.get())
        self.set_wordid(new_id)

    def set_wordid(self, new_id):
        '''
        Set the word ID and corresponding word, highlighting the word
        in the sentence Text.
        '''
        if 1 <= new_id <= len(self.segmentations):
            self.wordvar.set(new_id)
            self.word = self.segmentations[new_id-1]
            self.highlight_word(new_id-1)
            self.canvas.update()
#            self.show_segmentations()

    def init_sentence_text(self):
        '''
        Create the sentence Text and the word highligh tag.
        '''
        self.sent_text = Text(self, font=self.geez_big, width=SegRoot.sentencewidth, height=2, padx=20)
#        sl.tag_configure("align", justify='center')
        self.sent_text.insert("1.0", self.sentence)
        self.sent_text.tag_configure("highlight", background="OliveDrab1", foreground="black")
#        self.highlight_word(0)
#        sl.tag_add("align", "1.0", "end")
#        sl.tag_add("highlight", "1.0","1.4")
#        sl.tag_configure("highlight", background="OliveDrab1", foreground="black")

    def highlight_word(self, windex):
        '''
        Highlight the word in windex position in the sentence by reassigning the position
        of the highlight tag.
        (Alternately, have a separate tag for each word, allowing user to select word by
        by clicking.)
        '''
        positions = self.word_positions[windex]
#        tag = "highlight{}".format(windex)
        self.sent_text.tag_remove("highlight", "1.0", "end")
#        if windex > 0:
#            lasttag = "highlight{}".format(windex-1)
#            self.sent_text.tag_configure(lasttag, background="white", foreground="black")
        self.sent_text.tag_add("highlight", "1.{}".format(positions[0]), "1.{}".format(positions[1]))
#        self.sent_text.tag_configure("highlight", background="OliveDrab1", foreground="black")

    def set_sentence(self, sentindex):
        '''
        Set the segmentations of the current sentence.
        Delete the previous sentence and show the current one in the sentence Text.
        Set the positions of words within the sentence Text.
        Make the first word the current word.
        '''
        self.sentenceobj = self.corpus.sentences[sentindex]
        self.segmentations = self.sentenceobj.words
        self.sent_text.delete("1.0", "end")
        self.sent_text.insert("1.0", self.sentence)
        self.set_word_positions()
        self.set_wordid(1)

    def set_word_positions(self):
        '''
        Set the positions of the words within the current sentence.
        '''
        sentid = self.sentvar.get()-1
        if sentid in self.all_word_positions:
            positions = self.all_word_positions[sentid]
        else:
            words = self.sentence.split()
            positions = []
            position = 0
            for word in words:
                start = self.sentence.find(word, position)
                end = start + len(word)
                position = end
                positions.append((start, end))
            self.all_word_positions[sentid] = positions
        self.word_positions = positions

    def decrease_sentid(self):
        '''
        Decrease the current sentence ID.
        '''
        sentid = self.sentvar.get()
        new_id = sentid - 1
        self.set_sentid(new_id)

    def increase_sentid(self):
        '''
        Increase the current sentence ID.
        '''
        sentid = self.sentvar.get()
        new_id = sentid + 1
        self.set_sentid(new_id)

    def decrease_wordid(self):
        '''
        Decrease the current word ID.
        '''
        wordid = self.wordvar.get()
        new_id = wordid - 1
        self.set_wordid(new_id)

    def increase_wordid(self):
        '''
        Increase the current word ID.
        '''
        wordid = self.wordvar.get()
        new_id = wordid + 1
        self.set_wordid(new_id)

    def get_word_segmentations(self):
        '''
        Get the segmentations for the current word.
        '''
        wordindex = self.wordvar.get()-1
        wordsegs = self.segmentations[wordindex]
        return wordsegs

    def set_word_segmentations(self, newsegs):
        '''
        Update the segmentations for the current word (based on selection by user).
        '''
        self.sentenceobj.disambiguated = True
        wordindex = self.wordvar.get()-1
        self.segmentations[wordindex] = newsegs

class SegCanvas(Canvas):
    '''
    Canvas within the disambiguation window where segmentations are shown and selected.
    '''

    depYoffset = 10
    segIDwidth = 50
    segcolwidth = 125
    segrowheight = 18
    Y0 = 25
    segYmargin = 10
    segwidth = 400
    segdependencyheight = 20
    seggap = 40
    segrightmargin = 20
    deplabelX = 28
    deplabelY = 8

    def __init__(self, parent, corpus=None, width=800, height=600):
        Canvas.__init__(self, parent, width=width, height=height, bg="white")
        self.parent = parent
        self._width = width
        self._height = height
        self.columnX = []
        self.grid(row=2, columnspan=3, ipadx=15, ipady=15)
        self.update()
        self.grid()

    def clear(self):
        '''
        Clear the Canvas of all widgets.
        '''
        self.delete('all')

    def update(self):
        wordsegs = self.parent.get_word_segmentations()
        self.show_word(wordsegs)
        
    def show_word(self, wordsegs):
        '''
        Show a word's segmentations: forms, POS, features, dependency arcs, lemmas (if different from forms).
        '''
#        print("* Showing {}".format(wordsegs))
        self.clear()
        y = SegCanvas.Y0
        segYs = []
        # Maximum number of segments in a segmentation
        maxn = 0
        segIDtags = []
        segboxtags = []
        posselecttags = []
        nwordsegs = len(wordsegs)
        for segi, wordseg in enumerate(wordsegs):
            segYs.append(y - SegCanvas.segYmargin)
            word = Sentence.get_word(wordseg)
            headindex = Sentence.get_headindex(wordseg)
            forms = Sentence.get_forms(wordseg)
            lemmas = Sentence.get_lemmas(wordseg, forms, headindex)
            pos = Sentence.get_pos(wordseg)
            features = Sentence.get_features(wordseg)
            dependencies = Sentence.get_dependencies(wordseg)
            n = len(forms)
            maxn = max([maxn, n])
            Xs = self.get_columnX(n)
            # label for the segmentations; responds to mouse enter/leave and clicks
            if nwordsegs > 1:
                segboxtags.append(self.create_rectangle(SegCanvas.segIDwidth // 2 - 10, y - 10, SegCanvas.segIDwidth // 2 + 10, y + 10, fill='white'))
                segIDtags.append(self.create_text((SegCanvas.segIDwidth // 2, y), text=str(segi+1), font=self.parent.roman_big))
            # Put the dependencies at the top
            if dependencies:
                y = self.show_dependencies(dependencies, Xs, headindex, y)
            self.show_forms(forms, Xs, y)
            if pos:
                y += SegCanvas.segrowheight
                self.show_pos(pos, Xs, y, wordseg, posselecttags)
            if features:
                y += SegCanvas.segrowheight
                self.show_features(features, Xs, y)
            if lemmas:
                y += SegCanvas.segrowheight
                self.show_lemmas(lemmas, Xs, y)
            # Gap between segmentations
            if segi < len(wordsegs) - 1:
                y += SegCanvas.seggap
            else:
                # After last segmentation
                y += 31
        segYs.append(y)
        i = 0
        rightX = SegCanvas.segIDwidth + maxn * SegCanvas.segcolwidth
        if posselecttags:
            for seg, tag1, tag2, pos1, pos2 in posselecttags:
                self.tag_bind(tag1, "<Enter>", self.highlight_pos_handler(tag1, 'Red'))
                self.tag_bind(tag1, "<Leave>", self.highlight_pos_handler(tag1, 'Black'))
                self.tag_bind(tag2, "<Enter>", self.highlight_pos_handler(tag2, 'Red'))
                self.tag_bind(tag2, "<Leave>", self.highlight_pos_handler(tag2, 'Black'))
                self.tag_bind(tag1, "<ButtonRelease-1>", self.select_pos_handler(tag1, pos1, seg))
                self.tag_bind(tag2, "<ButtonRelease-1>", self.select_pos_handler(tag2, pos2, seg))
        if nwordsegs > 1:
            # Bind label boxes to handlers
            for index, (idtag, boxtag) in enumerate(zip(segIDtags, segboxtags)):
                self.tag_bind(idtag, "<ButtonRelease-1>", self.select_handler(wordsegs[index]))
                self.tag_bind(idtag, "<Enter>", self.highlight_box_handler(boxtag, 'LightPink'))
                self.tag_bind(idtag, "<Leave>", self.highlight_box_handler(boxtag, 'white'))
        # Rectangle around each segmentation
        while i < len(segYs) - 1:
            self.create_rectangle(SegCanvas.segIDwidth, segYs[i]-SegCanvas.segrowheight // 4, rightX, segYs[i+1]-18)
            i += 1
        # Adjusting the scroll region for the scrollbars based on new widgets
        self.configure(scrollregion=self.bbox("all"))

    def select_handler(self, seg):
        '''
        Returns the selection handler for the segmentation label.
        seg: the segmentation to be selected
        '''
        return lambda event: self.select(seg)

    def select(self, seg):
        '''
        Select seg as the segmentation for the current word.
        '''
        self.parent.set_word_segmentations([seg])
        self.update()
#        self.parent.show_segmentations()
        return seg

    def select_pos_handler(self, tag, pos, seg):
        return lambda event: self.select_pos(tag, pos, seg)

    def select_pos(self, tag, pos, seg):
#        print("** Setting tag {} POS {} for segment {}".format(tag, pos, seg))
        seg['upos'] = pos
        seg['xpos'] = pos
#        print("** Sentence {} updated ...".format(self.parent.sentenceobj))
        self.parent.sentenceobj.disambiguated = True
        self.update()
#        self.parent.show_segmentations()

    def highlight_pos_handler(self, posid, color):
        return lambda event: self.highlight_pos(posid, color)

    def highlight_pos(self, posid, color):
        self.itemconfigure(posid, fill=color)

    def highlight_box_handler(self, boxid, color):
        '''
        Returns the highlight and dehighlight handler for the segmentation label.
        '''
        return lambda event: self.highlight_box(boxid, color)

    def highlight_box(self, boxid, color):
        '''
        Highlight or dehighlight a segmentation label box.
        '''
#        print("** Highlighting {}".format(boxid))
        self.itemconfigure(boxid, fill=color)

    def get_columnX(self, n):
        '''
        The X coordinates for the columns in a segmentation display.
        '''
        start = SegCanvas.segIDwidth + SegCanvas.segcolwidth // 2
        X = []
        for i in range(n):
            X.append(start + i * SegCanvas.segcolwidth)
        return X

    def show_forms(self, forms, Xs, y):
        '''
        Show the forms for a segmentation.
        '''
        for form, x in zip(forms, Xs):
            self.create_text((x, y), text=form, font=self.parent.geez_normal)

    def show_lemmas(self, lemmas, Xs, y):
        '''
        Show the lemmas for a segmentation (if different from forms).
        '''
        for lemma, x in zip(lemmas, Xs):
            self.create_text((x, y), text=lemma, font=self.parent.geez_normal)

    def show_pos(self, pos, Xs, y, wordseg, posselecttags):
        '''
        Show the POS tags for a segmentation, including both UPOS and XPOS if they're different only.
        '''
        if len(wordseg) == 1:
            # Unsegmented word
            p = pos[0]
            x = Xs[0]
            if p in Sentence.selectpos:
                self.create_selectPOS(p, x, y, wordseg[0], posselecttags)
            else:
                id = self.create_text((x, y), text=p)
        else:
            for morphi, (p, x) in enumerate(zip(pos, Xs)):
                w = wordseg[morphi+1]
#                print("** Morph {}: {}".format(morphi, w))
                if p in Sentence.selectpos:
                    self.create_selectPOS(p, x, y, w, posselecttags)
                else:
                    id = self.create_text((x, y), text=p)

    def create_selectPOS(self, pos, x, y, wordseg, posselecttags):
        selectpos = Sentence.selectpos[pos]
        pos1 = selectpos[0]
        pos2 = selectpos[1]
        self.create_rectangle(x - 55, y - 8, x - 5, y + 8, fill='pink')
        id1 = self.create_text((x-30, y), text=pos1)
        self.create_rectangle(x + 5, y - 8, x + 55, y + 8, fill='pink')
        id2 = self.create_text((x+30, y), text=pos2)
        posselecttags.append((wordseg, id1, id2, pos1, pos2))

    def show_features(self, feats, Xs, y):
        '''
        Show the morphological features for a segmentation if there are any.
        '''
        for f, x in zip(feats, Xs):
            self.create_text((x, y), text=f)
    
    def show_dependencies(self, dependencies, Xs, headindex, y):
        """
        Show left and right dependency arcs.
        """
#        print("** left {} and right {} dependencies".format(dependencies[0], dependencies[1]))
        headX = Xs[headindex]
        dependencydiff = len(dependencies[0]) - len(dependencies[1])
        left = dependencies[0]
        right = dependencies[1]
        if dependencydiff > 0:
            left = left[dependencydiff:]
            # more left than right dependencies
            for dependency in dependencies[0][:dependencydiff]:
                self.show_dependency(headX, y, Xs[dependency[1]], dependency[0])
                y += SegCanvas.segdependencyheight
        elif dependencydiff < 0:
            right = right[-dependencydiff:]
            # more right than left dependencies
            for dependency in dependencies[1][:-dependencydiff]:
                self.show_dependency(headX, y, Xs[dependency[1]], dependency[0])
                y += SegCanvas.segdependencyheight
        for l, r in zip(left, right):
            self.show_dependency(headX, y, Xs[l[1]], l[0])
            self.show_dependency(headX, y, Xs[r[1]], r[0], startcircle=False)
            y += SegCanvas.segdependencyheight
        return y

    def show_dependency(self, x1, y, x2, label, startcircle=True):
        self.create_line(x1, y, x2, y, arrow=LAST)
        X = (x2 - x1) / 2 + x1
        if startcircle:
            self.create_oval(x1 - 2, y - 2, x1 + 2, y + 2, fill='black')
        self.create_rectangle(X - SegCanvas.deplabelX, y - SegCanvas.deplabelY,
                              X + SegCanvas.deplabelX, y + SegCanvas.deplabelY,
                              fill='yellow', outline='yellow')
        self.create_text(((x2 - x1) / 2 + x1, y), text=label, fill='black')
