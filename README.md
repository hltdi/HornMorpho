This is version 4.0 of ***HornMorpho***, a Python program that performs morphological analysis, generation, segmentation, and grapheme-to-phoneme conversion in various languages of the Horn of Africa.

<!--For information about using the program, see the manual that came with the distribution: *horn3.5_quick.pdf*.
-->

## Installation
To install HornMorpho, you can use either the distribution file, `HornMorpho-4.0.tar.gz`, or the wheel file, `HornMorpho-4.0-py3-none-any.whl`, both of which can be found in the `dist/` folder and the `Versions` folder.
To install from the distribution file, first extract the files from it. Then go to the top-level folder, `HornMorpho-4.0`, and do the following in a Python shell:

	python setup.py install

making sure that you are using some version of Python 3.
To install from the wheel file, do the following in a Python shell.

	pip install HornMorpho-4.0-py3-none-any.whl
	
(This assumes that you have [wheel](https://pypi.org/project/wheel/) installed.)

Then to use the program, in a Python shell, do

	import hm

If you have problems with installation, contact [gasser@indiana.edu](mailto:gasser@indiana.edu).

## Functions
### Morphological analysis
Morphological analysis takes a word and returns zero or more analyses, each consisting of the root, stem, or lemma of the word and a set of grammatical features.

**`hm.anal`**(*language*, *word*)  
`Options: raw=False, um=False`

**`hm.anal_file`**(*language*, *input_file*)   
`Options: output_file=None`

>- *language* is a string representing the language, 'amh' for Amharic for example.
- *word* is a string representation of the word in the standard orthography for the language.
- *input_file* is a path to the file to be analyzed.

>The function `hm.anal` attempts to analyze the input word morphologically. Words may be ambiguous, in which case there are multiple analyses. By default, for each analysis the function prints out the lemma, a gloss of the lemma if available, and a description of the grammatical features.

    >>> hm.anal('amh', "የቤታችን")
    word: የቤታችን
    POS: noun, lemma: ቤት|bet, gloss: house
     possessor: 1 plur
     other: definite, genitive
     
>To return the 'raw' internal analysis of the word, use the option `raw=True`. A  `list` of Python `dicts` is returned, one for each analysis (this is new in versions 4.0), with keys for lemma, gloss, and grammatical features ('gram').

>The grammatical features returned are in the form of a **feature structure**, a kind of `dict` with grammatical feature names as keys and their values as values. Among the features you may find useful are `sb` (subject), `tm` (tense-aspect-modality), `ob` (object). (A complete description of these features will appear soon.) 

    >>> hm.anal('amh', "የቤታችን", raw=True)
    [{'lemma': 'ቤት|bet', 'root': 'ቤት|bEt', 'gloss': 'house', 'gram': [-acc,cnj=None,+def,-dis,+gen,-itu,-plr,pos=n,poss=[+expl,+p1,-p2,+plr],pp=None,-prp,t=[eng=house],v=None]}]
    
>To output features from the [UniMorph project](http://www.unimorph.org/), use the option `um=True`. The UniMorph features are returned as a string of feature names separated by semicolons. (A description of the relevant UniMorph features will appear soon.) **The UniMorph option currently only works for Amharic and Tigrinya.**

    >>> hm.anal('amh', "የቤታችን", um=True)
    [{'lemma': 'ቤት|bet', 'root': 'ቤት|bEt', 'gloss': 'house', 'gram': 'N;GEN;PSS1P'}]
    
>For verbs and nouns derived from verbs, `hm.anal` also returns a representation of the root of the word.

    >>> hm.anal('amh', "ተፈቀደላት", um=True)
    [{'lemma': 'ፈቀደ|fǝqqǝdǝ', 'root': '<fqd:A>', 'gloss': 'permit,allow', 'gram': 'V;PFV;PASS;3;SG;MASC;ARGDA3SF'}]
    
>The function `hm.anal_file` analyzes the words in a file, printing out the analyses for each word. If *output_file* is specified, the results are written to that file. The options for `hm.anal`, `raw` and `um`, also apply.

## Morphological generation
Morphological generation takes a lemma and a set of grammatical features and returns zero or more word forms.

**`hm.gen`**(*language*, *lemma*)  
`Options: features=None, um=None`

>- *language* is a string abbreviation of a language.
- *lemma* is a string representation of a lemma.

>This function attempts to generate one or more words from the lemma provided. If no grammatical features are specified, a set of default features is used.

    >>> hm.gen('amh', "ፈቀደ")
    ['ፈቀደ|fǝqqǝdǝ']

>Features are specified using the options `features`, with a string representation of a feature structure of the type returned by `hm.anal`, or `um`, with a string representation of a set of UniMorph features. **The UniMorph option currently only works for Amharic and Tigrinya.**

    >>> hm.gen('amh', "ፈቀደ", features="[sb=[+p1,+plr],tm=imf,+neg]")
	["አንፈቅድም|'anfǝqdɨm"]

	>>> hm.gen('amh', "ፈቀደ", um="1;PL;IPFV;NEG")
	["አንፈቅድም|'anfǝqdɨm"]

## Segmentation
Morphological segmentation takes a word and returns a representation of the sequence of morphemes making up the word.

**`hm.seg`**(*language*, *word*)  
`Options: realize=False`

**`hm.seg_file`**(*language*, *input_file*)  
`Options: output_file=None`

>- *language* is a string representing the language, 'amh' for Amharic for example.
- *word* is a string representation of the word in the standard orthography for the language.
- *input_file* is a path to the file to be analyzed.

>The function `hm.seg` takes a language abbreviation and a word in conventional orthography and returns a segmentation of the word. Morphemes are separated by hyphens, with an indication of the grammatical features associated with each morpheme following it in parentheses. For Amharic verbs, the stem appears in curly brackets. Within the stem the root and the consonant-vowel template are separated by a plus sign.

	>>> hm.seg('amh', "አንፈቅድም")
	አንፈቅድም -- v:'an(neg1,sb=1p)-{fqd+1e23}(imprf)-m(neg2)
	
>With the option `realize=True`, the morphemes appear in Ge`ez orthography.

	>>> hm.seg('amh', "አንፈቅድም", realize=True)
	[['አን(neg1,sb=1p)-{ፈቅድ}(imprf)-ም(neg2)']]
	
>The function `hm.seg_file` behaves like `hm.anal_file` except that it prints out a segmentation of the words in the file instead of a morphological analysis.

## Grapheme-to-phoneme conversion
The Ge`ez orthography that is used for Ethio-Eritrean Semitic languages faithfully represents almost all aspects of the phonology of the languages. However, it fails to represent consonant gemination and vowel epenthesis. 

*Gemination* refers to the lengthening of consonants. In most Ethio-Eritrean Semitic languages, it is both a property of particular lexical items (ልብ *lɨbb*) and a feature of verb morphology. In rare cases, this can result in ambiguity (ይመታል *yɨmǝtal* 'he hits', *yɨmmǝttal* 'he is hit'). Gemination is also crucial for speech synthesis.

*Epenthesis* refers to the process of inserting a vowel to break up sequences of consonants. In the Ge`ez orthography, the sixth order characters represent both bare consonants and consonants followed by the epenthetic vowel *ɨ*. For example, the word ዝብርቅርቅ consists entirely of sixth order characters, and the epenthetic vowel is inserted in three places to make the word pronounceable: *zɨbrɨqrɨqq*. Although epenthesis is never used to distinguish words from one another, like gemination, it is important for speech synthesis.

**`hm.phon`**(*language*, *word*)  
`Options: gram=False`

**`hm.phon_file`**(*language*, *input_file*)  
`Options: output_file=None`

>- *language* is a string representing the language, 'amh' for Amharic for example.
- *word* is a string representation of the word in the standard orthography for the language.
- *input_file* is a path to the file to be analyzed.

>The function `hm.phon` takes a string abbreviation of a language and an orthographic representation of a word and prints out a romanized representation of the pronunciation of the word, including gemination and epenthesis, where appropriate. Note that there may be multiple possible pronunciations.

	>>> hm.phon('amh', "ይመታል")
	yɨmǝtal yɨmmǝttal 
	
>With the option `gram=True`,  `hm.phon` prints out grammatical information for each pronunciation.

	>>> hm.phon('amh', "ይመታል", gram=True)
	-- yɨmǝtal
	POS: verb, root: <mt':A>, gloss: strike,hit
	 subject: 3 sing mas
	 aspect/voice/tense: imperfective, aux:alle
	-- yɨmmǝttal
	POS: verb, root: <mt':A>, gloss: strike,hit
	 subject: 3 sing mas
	 aspect/voice/tense: imperfective, aux:alle, passive

> With the option `raw=True`, a `dict` is returned for each pronunciation, including the internal feature structure resulting from morphological analysis.

>The function `hm.phon_file` behaves like `hm.anal_file` and `hm.seg_file`.




