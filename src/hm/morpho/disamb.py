"""
This file is part of HornMorpho, which is part of the PLoGS project.

    <http://homes.soic.indiana.edu/gasser/plogs.html>

    Copyleft 2025.
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
Author: Michael Gasser <gasser@iu.edu>

Calling the external disambiguator model on sentences.
"""

import math, requests, json, sys, difflib

url = "http://213.55.95.103:11434/api/generate"
headers = {"Content-Type": "application/json"}
alpaca_prompt_2 =\
"""Below are possible analyses of a word. Choose the correct one.
### Instruction: {}
### Original Sentence: {}
### HM_Output: {}
### Amb_word: {}
### Disambiguated: {}"""

def disambiguate_sentence(sentence, verbosity=0):
    '''
    Run the disambiguator model on the ambiguous words in the
    sentence object.
    '''
    if verbosity:
        print("Calling disambiguator on {}". format(sentence))
    mini_sent = sentence.to_mini(tostring=False, include=True, indices=False)
    text = sentence.text
    formatted_words = []
    mini_word_options = []
    for mini_word, word in zip(mini_sent, sentence.words):
        token = word.name
        formatted_words.append(miniword2string(token, mini_word))
        mini_word_options.append([anal.__repr__() for anal in mini_word])
    formatted_sent = ' '.join(formatted_words)
    for word_i, (formatted_word, options, mini_word, word_obj) in enumerate(zip(formatted_words, mini_word_options, mini_sent, sentence.words)):
        if len(options) > 1:
            # the word is ambiguous
            disamb_i, disamb_option = disambiguate_word(text, formatted_sent, options, formatted_word)
            if disamb_option:
                # the model gave an interpretable response
                word_obj.model_disamb = disamb_i
#                sentence.model_disamb[word_i] = disamb_i

def disambiguate_word(original, formatted_sent, word_options, formatted_word, verbosity=0):
    if verbosity:
        print("  Calling disambiguator on {}".format(formatted_word))
    prompt = format_prompt(original, formatted_sent, formatted_word)
    payload = {
        "model": "disambig_latest",  
        "prompt": prompt,
        "stream": False
        }
    response = requests.post(url, headers=headers, data=json.dumps(payload, ensure_ascii=False))    
    result = response.json()  
    chosen_option = result.get("response").strip()
    if verbosity:
        print("  ** chosen {}".format(chosen_option))
    try:
        which_option = word_options.index(chosen_option)
        if verbosity:
            print("  ** found match: {}".format(which_option))
        return which_option, chosen_option
    except ValueError:
        close_matches = difflib.get_close_matches(chosen_option, word_options, n=1, cutoff=0.6)
        if (len(close_matches)>0):
            if verbosity:
                print("  ** found close match {}".format(close_matches[0]))
            return -1, close_matches[0]
        else:
            return -1, ""


def miniword2string(token, analyses):
    '''
    Convert a miniature representation of a word's analyses -- a list of token, lemma, POS, feats lists --
    to a string suitable for the model.
    '''
    return token + "<" + analyses.__repr__() + ">"

def minisentence2string(words):
    '''
    Convert a miniature representation of a sentence -- a list of miniature word representations --
    to a string suitable for the model.
    '''
    result = []
    for word in words:
        token = word[0][0]
        result.append(miniword2string(token, word))
    return ' '.join(result)

def format_prompt(original, hm_output, amb_word):
    fixed_instruction = "ለተሰጠው ቃል ትክክለኛውን ሲንታክስ ምረጥ። "
    text = alpaca_prompt_2.format(fixed_instruction, original, hm_output, amb_word,"") + "<end_of_text>"
    return text

## Abnet's code
##
##def disambiguate(original, hm_output, amb_word):
##    '''
##    Sample Input:
##    original = "ወጥ አውጪ !"
##    hm_output = "ወጥ<['ወጥ', 'ወጥ', 'NOUN', {}]> አውጪ<[['አውጪ', 'አወጣ', 'VERB', {'Gender': 'Fem', 'Mood': 'Imp', 'Number': 'Sing', 'Person': '2',  
##              'Voice': 'Cau'}], ['አውጪ', 'አውጭ', 'ADJ', {}]]> !<['!', '!', 'PUNCT', {}]>"
##    amb_word = "አውጪ<[['አውጪ', 'አውጭ', 'ADJ', {}], ['አውጪ', 'አወጣ', 'VERB', {'Gender': 'Fem', 'Mood': 'Imp', 'Number': 'Sing', 'Person': '2', 'Voice':
##             'Cau'}]]>"
##    '''
##    prompt = format_prompt(original, hm_output, amb_word)
##    options = amb_word.split("],")
##    refined_options = []
##    for i, option in enumerate(options):
##        if (i==0):
##            refined_options.append(option.split("<[")[1] + "]".strip())
##        elif (i==len(options)-1):
##            refined_options.append(option.split("]>")[0].strip())
##        else:
##            refined_options.append((option+"]").strip())
##    payload = {
##        "model": "disambig_1670",  
##        "prompt": prompt,
##        "stream": False
##        }
##    response = requests.post(url, headers=headers, data=json.dumps(payload, ensure_ascii=False))    
##    result = response.json()  
##    chosen_option = result.get("response").strip()
##    try:
##        which_option = refined_options.index(chosen_option)
##        return chosen_option
##    except ValueError:
##        close_matches = difflib.get_close_matches(chosen_option, refined_options, n=1, cutoff=0.6)
##        if (len(close_matches)>0):
##            return close_matches[0]
##        else:
##            return ""

##def test():
##    with open ("../tmp/starter_disambigs_word3.json", "r", encoding="utf-8") as file:
##        test_dataset = json.load(file)
##    cnt_correct = 0; cnt_total = 0
##    for t in test_dataset[1670:1675]: #Run only the first 5 test samples (test_data starts from index 1670)
##        cnt_total+=1
##        chosen_option = disambiguate(t["original"], t["hm_output"], t["amb_word"])
##        if (chosen_option == t["disambig_word"]): 
##            print("\nThe model CORRECTLY disambiguated ",t["amb_word"].split("<[")[0], " from ", t["original"]); 
##            print(chosen_option)
##            cnt_correct+=1 
##        else: 
##            print("\nThe model INCORRECTLY disambiguated ",t["amb_word"].split("<[")[0], " from ", t["original"])
##            print("What was correct ", t["disambig_word"])
##            print("What was chosen ", chosen_option)
##    print("\n")       
##    print(cnt_correct, " was correctly disambiguated out of ", cnt_total)
##    print("Accuracy ", cnt_correct/cnt_total)

