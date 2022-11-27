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
# import tkinter.ttfont

class Corpus():
    """
    List of tokenized sentences to be segmented and displayed.
    """

    ID = 0

    def __init__(self, data=None, file='', name=''):
        self.data = data
        self.segmentations = []
        self.name = name or self.create_name()

    def __repr__(self):
        return "C_{}".format(self.name)

    def create_name(self):
        name = "{}".format(Corpus.ID)
        Corpus.ID += 1
        return name

    def disambiguate(self):
        '''
        Show the segmentations in the GUI so words with multiple
        segmentations can be disambiguated.
        '''
        if not self.segmentations:
            # Segment all sentences before creating GUI.
            self.segment_all()
        root = Tk()
        root.grid_columnconfigure(0, weight=1)
        self.frame = SegFrame(root, self, title=self.__repr__())
#        fontfamilies = families()
#        print("families {}".format(fontfamilies[:100]))
        self.frame.mainloop()

    def segment_all(self):
        """
        Segment all the sentences in self.data.
        % Later have the option of segmenting only some??
        """
        language = get_language('amh', phon=False, segment=True, experimental=True)
        print("Segmenting sentences in {}".format(self))
        for sentence in self.data:
            segmentations = language.anal_sentence(sentence)
            self.segmentations.append(segmentations)

    def segment(self, sentence='', sentindex=0, language='amh'):
        """
        Segment one sentence. (This may not be needed.)
        """
        if sentindex in self.all_segmentations:
            segmentations = self.all_segmentations[sentindex]
        else:
            sentence = sentence or self.data[sentindex] if sentindex < len(self.data) else None
            if sentence:
                language = get_language(language, phon=False, segment=True, experimental=True)
                segmentations = language.anal_sentence(sentence)
                if segmentations:
                    self.all_segmentations[sentindex] = segmentations
        if segmentations:
            self.frame.segmentations = segmentations.words
        return segmentations

class SegFrame(Frame):
    '''
    Frame for the disambiguation GUI.
    '''

    # width of column for showing segmentation ID
    segid_width = 40
    # gap between column centers for tokens and their properties
    token_gap = 100

    def __init__(self, parent, corpus=None, width=700, height=800, title=None):
        Frame.__init__(self, parent, width=width, height=height)
        parent.title(title if title else "Corpus")
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
        self.geez_big = Font(family="Abyssinica SIL", size=20)
        self.geez_normal = Font(family="Abyssinica SIL", size=18)
        self.roman_big = Font(family="Arial", size=20)
        self.init_sentence_text()
        self.id_frame = Frame(self, width=200, height=100)
        self.wordid_entry = self.init_wordid_entry()
        self.sentid_entry = self.init_sentid_entry()
        self.id_frame.grid(row=0, column=0)
#        self.segment_button = Button(self, text="Segment sentence", command=self.segment)
#        self.segment_button.grid(row=0, column=2)
        self.show_button = Button(self, text="Show segmentations", command=self.show_segmentations)
        self.show_button.grid(row=0, column=2)
        self.sent_text.grid(row=1, columnspan=3)
        self.canvas = SegCanvas(self, corpus, width=width-25, height=height-25)
        self.grid()
#        self.show_segmenting()
        self.segmentations = self.corpus.segmentations[sentindex].words

#    def segment(self):
#        print("{}".format(self.sentence))
#        self.corpus.segment(self.sentence)

#    def show_segmenting(self):
#        self.segmenting = self.canvas.create_text((100, 300), text="Segmenting...", font=self.roman_big)

    def init_vars(self):
        self.sentvar = IntVar()
        self.sentvar.set(1)
        self.wordvar = IntVar()
        self.wordvar.set(1)

    def init_sentid_entry(self):
        sentframe = Frame(self.id_frame, width=25, height=100)
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
        wordframe = Frame(self.id_frame, width=25, height=100)
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
        new_id = int(self.sentid_entry.get())
        self.set_sentid(new_id)

    def set_sentid(self, new_id):
        if 1 <= new_id <= len(self.corpus.data):
            self.sentvar.set(new_id)
            self.sentence = self.corpus.data[new_id-1]
            self.set_sentence(new_id-1)

    def get_wordid(self, event):
        new_id = int(self.wordid_entry.get())
        self.set_wordid(new_id)

    def set_wordid(self, new_id):
        if 1 <= new_id <= len(self.segmentations):
            self.wordvar.set(new_id)
            self.word = self.segmentations[new_id-1]
            self.highlight_word(new_id-1)

    def init_sentence_text(self):
        self.sent_text = Text(self, font=self.geez_big, width=60, height=2, padx=20)
#        sl.tag_configure("align", justify='center')
        self.sent_text.insert("1.0", self.sentence)
        self.sent_text.tag_configure("highlight", background="OliveDrab1", foreground="black")
#        self.highlight_word(0)
#        sl.tag_add("align", "1.0", "end")
#        sl.tag_add("highlight", "1.0","1.4")
#        sl.tag_configure("highlight", background="OliveDrab1", foreground="black")

    def highlight_word(self, windex):
        positions = self.word_positions[windex]
#        tag = "highlight{}".format(windex)
        self.sent_text.tag_remove("highlight", "1.0", "end")
#        if windex > 0:
#            lasttag = "highlight{}".format(windex-1)
#            self.sent_text.tag_configure(lasttag, background="white", foreground="black")
        self.sent_text.tag_add("highlight", "1.{}".format(positions[0]), "1.{}".format(positions[1]))
#        self.sent_text.tag_configure("highlight", background="OliveDrab1", foreground="black")

    def set_sentence(self, sentindex):
        self.segmentations = self.corpus.segmentations[sentindex].words
        self.sent_text.delete("1.0", "end")
        self.sent_text.insert("1.0", self.sentence)
        self.set_word_positions()
#        self.word_positions = SegFrame.get_word_positions(self.sentence)
        self.set_wordid(1)

#    @staticmethod
#    def get_word_positions(sentence):
#        words = sentence.split()
#        positions = []
#        position = 0
#        for word in words:
#            start = sentence.find(word, position)
#            end = start + len(word)
#            position = end
#            positions.append((start, end))
##        print("** word positions {}".format(positions))
#        return positions

    def set_word_positions(self):
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
#        print("** word positions {}".format(positions))
        self.word_positions = positions

    def decrease_sentid(self):
        sentid = self.sentvar.get()
        new_id = sentid - 1
        self.set_sentid(new_id)

    def increase_sentid(self):
        sentid = self.sentvar.get()
        new_id = sentid + 1
        self.set_sentid(new_id)

    def decrease_wordid(self):
        wordid = self.wordvar.get()
        new_id = wordid - 1
        self.set_wordid(new_id)

    def increase_wordid(self):
        wordid = self.wordvar.get()
        new_id = wordid + 1
        self.set_wordid(new_id)

    def get_word_segmentations(self):
        wordindex = self.wordvar.get()-1
        wordsegs = self.segmentations[wordindex]
        return wordsegs

    def show_segmentations(self):
        if not self.segmentations:
            print("** No segmentations to show")
            return
        wordsegs = self.get_word_segmentations()
        self.canvas.show_word(wordsegs)

    def set_word_segmentations(self, newsegs):
        wordindex = self.wordvar.get()-1
        print("** Setting word segmentations for word {}".format(wordindex))
        print("** Old:\n{}".format(self.segmentations[wordindex]))
        print("** New:\n{}".format(newsegs))
        self.segmentations[wordindex] = newsegs

#    def highlight_word(self, 

class SegCanvas(Canvas):

#    boundary = 25
    depYoffset = 10
    segIDwidth = 50
    segcolwidth = 100
    segrowheight = 18
    Y0 = 25
    segYmargin = 10
    segwidth = 400
    segarcheight = 20
    seggap = 40
    segrightmargin = 20
    deplabelX = 15
    deplabelY = 8

    def __init__(self, parent, corpus=None, width=600, height=600):
        Canvas.__init__(self, parent, width=width, height=height, bg="white")
        self.frame = parent
        self._width = width
        self._height = height
        self.columnX = []
#        self.show_morphs(["ይ", "ሰማ", "ኣል"])
#        self.show_arc(50, 200, 200, 200, "nsubj")
        self.grid(row=2, columnspan=3)
#        self.pack()

    def clear(self):
        self.delete('all')
        
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
        nwordsegs = len(wordsegs)
        for segi, wordseg in enumerate(wordsegs):
            segYs.append(y - SegCanvas.segYmargin)
#            print(" ** Showing {}".format(wordseg))
            word = Sentence.get_word(wordseg)
            headindex = Sentence.get_headindex(wordseg)
            forms = Sentence.get_forms(wordseg)
            lemmas = Sentence.get_lemmas(wordseg, forms)
            pos = Sentence.get_pos(wordseg)
            features = Sentence.get_features(wordseg)
            arcs = Sentence.get_arcs(wordseg)
            n = len(forms)
            maxn = max([maxn, n])
            Xs = self.get_columnX(n)
            # labels for the different segmentations; respond to mouse enter/leave and clicks
            if nwordsegs > 1:
                segboxtags.append(self.create_rectangle(SegCanvas.segIDwidth // 2 - 10, y - 10, SegCanvas.segIDwidth // 2 + 10, y + 10, fill='white'))
                segIDtags.append(self.create_text((SegCanvas.segIDwidth // 2, y), text=str(segi+1), font=self.frame.roman_big))
#            print(" *** {}:{}:{} {} {} {} {} {}".format(word, headindex, lemmas, forms, pos, features, arcs, Xs))
            # Put the dependencies at the top
            if arcs:
                y = self.show_arcs(arcs, Xs, headindex, y)
            self.show_forms(forms, Xs, y)
            if pos:
                y += SegCanvas.segrowheight
                self.show_pos(pos, Xs, y)
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
#        print(" **** segboxtags {}".format(segboxtags))
        if n > 1:
            # Bind label boxes to handlers
            for index, (idtag, boxtag) in enumerate(zip(segIDtags, segboxtags)):
                self.tag_bind(idtag, "<ButtonRelease-1>", self.select_handler(wordsegs[index]))
                self.tag_bind(idtag, "<Enter>", self.highlight_box_handler(boxtag, 'pink'))
                self.tag_bind(idtag, "<Leave>", self.highlight_box_handler(boxtag, 'white'))
        # Rectangle around each segmentation
        while i < len(segYs) - 1:
            self.create_rectangle(SegCanvas.segIDwidth, segYs[i]-SegCanvas.segrowheight // 4, rightX, segYs[i+1]-18)
            i += 1

    def select_handler(self, segs):
        return lambda event: self.select(segs)

    def select(self, segs):
        self.frame.set_word_segmentations([segs])
        return segs

    def highlight_box_handler(self, boxid, color):
        return lambda event: self.highlight_box(boxid, color)

    def highlight_box(self, boxid, color):
        self.itemconfigure(boxid, fill=color)

    def get_columnX(self, n):
#        center = (self._width - SegCanvas.segIDwidth) // 2 + SegCanvas.segIDwidth
#        start = center - SegCanvas.segcolwidth * (n-1) // 2
        start = SegCanvas.segIDwidth + SegCanvas.segcolwidth // 2
        X = []
        for i in range(n):
            X.append(start + i * SegCanvas.segcolwidth)
        return X

    def show_forms(self, forms, Xs, y):
        for form, x in zip(forms, Xs):
            self.create_text((x, y), text=form, font=self.frame.geez_normal)

    def show_lemmas(self, lemmas, Xs, y):
        for lemma, x in zip(lemmas, Xs):
            self.create_text((x, y), text=lemma, font=self.frame.geez_normal)

    def show_pos(self, pos, Xs, y):
        for p, x in zip(pos, Xs):
            self.create_text((x, y), text=p)

    def show_features(self, feats, Xs, y):
        for f, x in zip(feats, Xs):
            self.create_text((x, y), text=f)
    
#    def show_form(self, form, x, y):
#        self.create_text((x, y), text=form, font=self.frame.geez_normal)

#    def show_morphs(self, morphs):
#        for i, morph in enumerate(morphs):
#            self.show_form(morph, i*100, 100)

#    def calc_seg_X(self, nmorphs):
#        xwidth = self._width - 2 * SegCanvas.boundary
#        x0 = SegCanvas.boundary

    def show_arcs(self, arcs, Xs, headindex, y):
        """
        Show left and right dependency arcs.
        """
        headX = Xs[headindex]
        arcdiff = len(arcs[0]) - len(arcs[1])
        left = arcs[0]
        right = arcs[1]
        if arcdiff > 0:
            left = left[arcdiff:]
            # more left than right arcs
            for arc in arcs[0][:arcdiff]:
                self.show_arc(headX, y, Xs[arc[1]], arc[0])
                y += SegCanvas.segarcheight
        elif arcdiff < 0:
            right = right[arcdiff:]
            for arc in arcs[1][:-arcdiff]:
                self.show_arc(headX, y, Xs[arc[1]], arc[0])
                y += SegCanvas.segarcheight
        for l, r in zip(left, right):
            self.show_arc(headX, y, Xs[l[1]], l[0])
            self.show_arc(headX, y, Xs[r[1]], r[0], startcircle=False)
            y += SegCanvas.segarcheight
        return y

    def show_arc(self, x1, y, x2, label, startcircle=True):
        self.create_line(x1, y, x2, y, arrow=LAST)
        X = (x2 - x1) / 2 + x1
        if startcircle:
            self.create_oval(x1 - 2, y - 2, x1 + 2, y + 2, fill='black')
        self.create_rectangle(X - SegCanvas.deplabelX, y - SegCanvas.deplabelY,
                              X + SegCanvas.deplabelX, y + SegCanvas.deplabelY,
                              fill='yellow', outline='yellow')
#        self.create_text(((x2 - x1) / 2 + x1, y - SegCanvas.depYoffset), text=label, fill='black')
        self.create_text(((x2 - x1) / 2 + x1, y), text=label, fill='black')

#    def geez(self, text, x, y):
#        return self.create_text(x, y, text=text, fill="Black", font=self.geez_font)
