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

GUI for displaying and disambiguating sentences.
"""
from tkinter import *
from tkinter.ttk import *
from tkinter.font import *
from .sentence import Sentence

class SegRoot(Tk):
    '''
    Main window for the disambiguation GUI.
    '''

    sentencewidth = 60

    def __init__(self, corpus=None, title=None): # parent, corpus=None, width=1000, height=300, title=None):
        Tk.__init__(self) #, parent) #, width=width, height=height)
        self.title(title if title else "Corpus")
        fontfamilies = families()
        geezfamily =  "Abyssinica SIL" if "Abyssinica SIL" in fontfamilies else "Noto Sans Ethiopic"
#        print("families {}".format(fontfamilies[150:300]))
        self.corpus = corpus
        # Create int variables for sentence and word index (1-based)
        self.init_vars()
        sentindex = self.sentvar.get()-1
        self.sentenceGUIs = {}
        # Find the sentence in the corpus
        if not corpus.data:
            print("No data in corpus!")
            return
        if not corpus.sentences:
            print("No sentences in corpus!")
            return
        sentence = corpus.data[sentindex]
        sentenceobj = self.corpus.sentences[sentindex]
        self.always_paint = True
        # Fonts
        self.geez_big = Font(family=geezfamily, size=20)
        self.geez_normal = Font(family=geezfamily, size=16)
        self.roman_big = Font(family="Arial", size=20)
        self.roman_medium = Font(family="Arial", size=18)
        # Sentence Label and Text
        self.init_sentence_text()
        # Undo and Quit buttons
        self.init_buttons()
        # Canvas and scrollbars
        self.canvas = SegCanvas(self, corpus) # width=width-25, height=height-25)
        self.scrollbar = Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scrollbar.grid(row=2, column=3, sticky='ns')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.hscrollbar = Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.hscrollbar.grid(row=3, columnspan=3, sticky='ew')
        self.canvas.configure(xscrollcommand=self.hscrollbar.set)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        # First sentenceGUI
        self.sentenceGUI = \
          SentenceGUI(frame=self, canvas=self.canvas, sentence=sentence,
                      sentenceobj=sentenceobj, index=sentindex)
        self.sentenceGUI.show_sentence(True)
        self.sentenceGUI.show_unambig()
        self.canvas.update()
        self.wordid_entry = self.init_wordid_entry()
        self.sentid_entry = self.init_sentid_entry()
        self.bind('<Left>', self.decr_wordid_handler())
        self.bind('<Right>', self.incr_wordid_handler())

    def quit(self):
        '''
        Quit the GUI, destroying all widgets.
        '''
        self.destroy()

    def enable_undo(self):
        self.undo_button.configure(style="Active.TButton")
        self.undo_button["state"] = "normal"

    def disable_undo(self):
        self.undo_button.configure(style="Inactive.TButton")
        self.undo_button["state"] = "disabled"

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
        we.bind("<Return>", self.set_wordid)
        wordframe.grid(row=0, column=1, padx=10)
        self.sentenceGUI.highlight_word(0)
        return we

    def init_buttons(self):
        '''
        Create buttons for quitting and undoing.
        '''
        self.button_frame = Frame(self, width=25, height=100)
        active_style = Style()
        active_style.configure("Active.TButton", foreground='black')
        inactive_style = Style()
        inactive_style.configure('Inactive.TButton', foreground='LightGray')
        self.undo_button = Button(self.button_frame, text="Undo", command=self.undo, style='Inactive.TButton')
        self.quit_button = Button(self.button_frame, text="Quit", command=self.quit)
        self.undo_button.grid(row=0, column=0)
        self.quit_button.grid(row=1, column=0)
        self.button_frame.grid(row=0, column=2, padx=10)

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
            self.set_sentence(new_id-1)

    def set_wordid(self, event):
        '''
        Get the current word ID (1 greater than actual ID).
        '''
        new_id = int(self.wordid_entry.get())
        self.sentenceGUI.set_wordid(new_id)

    def init_sentence_text(self):
        '''
        Create the sentence Text and the word highlight tag.
        '''
        self.sent_frame = Frame(self, padding=10)
        self.sent_text = Text(self.sent_frame, font=self.geez_big, width=SegRoot.sentencewidth, height=2, padx=20)
        self.sent_label = Label(self.sent_frame, font=self.roman_medium) #, text=self.sentenceobj.label)
        self.sent_label.grid(row=0, column=0)
        self.sent_text.grid(row=1, column=0)
        self.sent_frame.grid(row=1, columnspan=3)

    def set_sentence(self, sentindex):
        '''
        Set the current sentence, creating a new SentenceGUI instance if there isn't
        already one in self.sentenceGUIs.
        Delete the previous sentence and show the current one in the sentence Text.
        Make the first word the current word.
        '''
        sentence = self.corpus.data[sentindex]
        sentenceobj = self.corpus.sentences[sentindex]
        if sentindex in self.sentenceGUIs:
            self.sentenceGUI = self.sentenceGUIs[sentindex]
        else:
            self.sentenceGUI = \
              SentenceGUI(frame=self, canvas=self.canvas, sentence=sentence,
                          sentenceobj=sentenceobj, index=sentindex)
        self.sentenceGUI.show_sentence()
        self.sentenceGUI.show_unambig(True)
        self.sentenceGUI.set_wordid(1, False)

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
        self.sentenceGUI.set_wordid(new_id)

    def increase_wordid(self):
        '''
        Increase the current word ID.
        '''
        wordid = self.wordvar.get()
        new_id = wordid + 1
        self.sentenceGUI.set_wordid(new_id)

    def incr_wordid_handler(self):
        return lambda event: self.increase_wordid()

    def decr_wordid_handler(self):
        return lambda event: self.decrease_wordid()

    def get_word_segmentations(self):
        '''
        Get the segmentations for the current word.
        '''
        wordindex = self.wordvar.get()-1
        wordsegs = self.sentenceGUI.words[wordindex]
        return wordsegs

    def undo(self):
        """
        Undo the last segmentation or POS selection.
        """
        self.sentenceGUI.undo()

class SegCanvas(Canvas):
    '''
    Canvas within the disambiguation window where segmentations are shown and selected.
    '''

    depYoffset = 10
    segIDwidth = 55
    segcolwidth = 125
    segrowheight = 18
    Y0 = 25
    segYmargin = 10
    segwidth = 400
    segdependencyheight = 20
    seggap = 40
    segrightmargin = 20
    deplabelX = 40
    deplabelY = 8

    def __init__(self, parent, corpus=None, width=800, height=600):
        Canvas.__init__(self, parent, width=width, height=height, bg="white")
        self.parent = parent
        self._width = width
        self._height = height
        self.columnX = []
        self.grid(row=2, columnspan=3, ipadx=15, ipady=15)
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
        self.parent.sentenceGUI.set_word_segmentations([seg])
        self.update()
        return seg

    def select_pos_handler(self, tag, pos, seg):
        '''
        Returns the handler for selecting POS on the POS labels.
        '''
        return lambda event: self.select_pos(pos, seg)

    def select_pos(self, pos, seg):
        '''
        Select pos as the POS for segmentation seg.
        '''
        self.parent.sentenceGUI.set_pos(pos, seg)
        self.update()

    def highlight_pos_handler(self, posid, color):
        '''
        Returns the handler for highlighting/dehighlighting the POS label on mouse Enter.
        '''
        return lambda event: self.highlight_pos(posid, color)

    def highlight_pos(self, posid, color):
        '''
        Highlight or dehighlight the POS label.
        '''
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
                if p in Sentence.selectpos:
                    self.create_selectPOS(p, x, y, w, posselecttags)
                else:
                    id = self.create_text((x, y), text=p)

    def create_selectPOS(self, pos, x, y, wordseg, posselecttags):
        '''
        Create POS labels to select between when there is a choice.
        '''
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
        '''
        Show a single dependency arc.
        '''
        self.create_line(x1, y, x2, y, arrow=LAST)
        X = (x2 - x1) / 2 + x1
        if startcircle:
            self.create_oval(x1 - 2, y - 2, x1 + 2, y + 2, fill='black')
        self.create_rectangle(X - SegCanvas.deplabelX, y - SegCanvas.deplabelY,
                              X + SegCanvas.deplabelX, y + SegCanvas.deplabelY,
                              fill='white', outline='black')
        self.create_text(((x2 - x1) / 2 + x1, y), text=label, fill='black')

class SentenceGUI():
    '''
    Keeps track of widgets and various features associated with a single sentence.
    '''

    # colors for word tags
    disambig = "OliveDrab1"
    unambig = "LightGray"

    def __init__(self, frame=None, canvas=None, sentence=None, sentenceobj=None, index=0):
        self.frame = frame
        self.canvas = canvas
        self.sentence = sentence
        self.sentenceobj = sentenceobj
        self.words = sentenceobj.words
        self.ambig = self.sentenceobj.record_ambiguities()
        self.index = index
        self.memory = []
        self.wordid = 0
        self.word = self.words[0]
        self.text = self.frame.sent_text
        self.label = self.frame.sent_label
        self.memory = {}
        self.set_word_strings()
        self.set_word_positions()
#        self.show_sentence(True)
#        self.make_word_tags()
        self.frame.sentenceGUIs[index] = self

    def show_sentence(self, first=False):
        '''
        Show the sentence in the sentence Text and sentence
        label in the sentence Label.
        If update is True, clear the sentence Text first,
        remove tags, recreate tags, and update the Undo button.
        '''
        self.text.insert("1.0", self.sentence)
        if not first:
            # First clear the sentence Text
            self.text.delete("1.{}".format(len(self.sentence)), "end")
            # And delete the old tags
            for tag in self.text.tag_names():
                self.text.tag_remove(tag, "1.0", "end")
        self.make_word_tags()
        if 0 in self.memory and self.memory[0]:
            self.frame.enable_undo()
        else:
            self.frame.disable_undo()
        self.label.config(text=self.sentenceobj.label)

    def set_wordid(self, new_id, update=True):
        '''
        Update the current word id. If update is True, set the background
        color of the new and old words.
        '''
        if 1 <= new_id <= len(self.words):
            old_id = self.wordid+1
            self.frame.wordvar.set(new_id)
            self.wordid = new_id-1
            self.word = self.words[new_id-1]
            self.canvas.update()
            if update:
                self.highlight_word(new_id-1)
                self.dehighlight_word(old_id-1)

    def set_word_strings(self):
        '''
        Assign the word strings in the sentence, either individual
        tokens or multi-word expressions.
        '''
        self.word_strings = []
        for index, word in enumerate(self.words):
            seg0 = word[0]
            whole_word = seg0[0]
            word_string = whole_word['form']
            self.word_strings.append(word_string)

    def set_word_positions(self):
        '''
        Set the positions of the word strings within the sentence.
        '''
        self.word_positions = []
        position = 0
        for word_string in self.word_strings:
            start = self.sentence.find(word_string, position)
            end = start + len(word_string)
#            print("** positions for {}: {}->{}".format(word_string, start, end))
            position = end
            self.word_positions.append((start, end))

    def make_word_tags(self):
        '''
        Create tags in the sentence Text for each word string and assign their initial colors.
        '''
        for index, (pos0, pos1) in enumerate(self.word_positions):
            self.text.tag_add("word{}".format(index), "1.{}".format(pos0), "1.{}".format(pos1))
            if index == 0:
                self.text.tag_configure("word{}".format(index), underline=1)
            else:
                self.text.tag_configure("word{}".format(index), underline=0)
            self.text.tag_configure("word{}".format(index), background=self.get_word_tag_color(index))

    def get_word_tag_color(self, index):
        '''
        Get the appropriate tag color for the word string at index.
        '''
        if index in self.memory and self.memory[index]:
            return SentenceGUI.disambig
        if index not in self.ambig:
            return SentenceGUI.unambig
        return "White"
        
    def highlight(self):
        '''
        Highlight the sentence Text for an unambiguous word.
        '''
        self.text.config(background='LightGray')
        self.label.config(foreground='Gray')

    def unhighlight(self):
        '''
        Unhighlight the sentence Text for an ambiguous word.
        '''
        self.text.config(background='white')
        self.label.config(foreground='black')

    def highlight_word(self, index):
        '''
        Underline the word at index (the current word) and set enable or disable
        the Undo button depending on whether the word's action memory.
        '''
        self.text.tag_configure("word{}".format(index), underline=1)
        if self.memory.get(index):
            self.frame.enable_undo()
        else:
            self.frame.disable_undo()

    def dehighlight_word(self, index):
        '''
        Remove the underline from a word that is not longer the current word.
        '''
        self.text.tag_configure("word{}".format(index), underline=0)

    def show_unambig(self, show_ambig=False):
        '''
        Indicate by the sentence Text background color whether the entire
        sentence is umambiguous or not.
        '''
        if not self.ambig:
            self.highlight()
        elif show_ambig:
            self.unhighlight()

    def set_pos(self, pos, seg):
        '''
        Update the POS tags for a segmentation (dict) for the current word, based on selection by user.
        Update the word's action memory, set the color for the word, enable the Undo button.
        '''
        self.sentenceobj.disambiguated = True
        old = ((seg['upos'], seg['xpos']), seg)
        if self.wordid in self.memory:
            self.memory[self.wordid].append(old)
        else:
            self.memory[self.wordid] = [old]
        self.show_disambig_word(self.wordid)
        self.frame.enable_undo()
        seg['upos'] = pos
        seg['xpos'] = pos

    def show_disambig_word(self, index):
        '''
        Set the color for the word at index to show that it's been disambiguated.
        '''
        self.text.tag_configure("word{}".format(index), background=SentenceGUI.disambig)

    def set_word_segmentations(self, newsegs):
        '''
        Update the segmentations for the current word (based on selection by user).
        Update the word's action memory, set the color for the word, enable the Undo button.
        '''
        self.sentenceobj.disambiguated = True
        wordindex = self.frame.wordvar.get()-1
        old = (wordindex, self.words[wordindex])
        if self.wordid in self.memory:
            self.memory[self.wordid].append(old)
        else:
            self.memory[self.wordid] = [old]
        self.show_disambig_word(self.wordid)
        self.frame.enable_undo()
        self.words[wordindex] = newsegs

    def undo(self):
        '''
        Undo the most recent action in the current word's memory.
        If the memory is empty, update the word's background color and Undo button.
        '''
        memory = self.memory.get(self.wordid)
        if not memory:
            print("Something wrong; nothing to undo!")
            return
        x, y = memory.pop()
        if isinstance(x, int):
            # This is a segmentation selection; x is the index, y the oldsegmentations
            self.words[x] = y
        else:
            # This is a POS selection; x is the old UPOS and XPOS, y the word dict
            upos, xpos = x
            y['upos'] = upos
            y['xpos'] = xpos
        if not memory:
            self.text.tag_configure("word{}".format(self.wordid), background='White')
            self.frame.disable_undo()
        self.canvas.update()