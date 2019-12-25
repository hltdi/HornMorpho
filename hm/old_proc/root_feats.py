### Analyze words in file using both lexical and guesser analyzers, recording known
### and new roots and their lexical properties.

def anal(morpho, word):
    anals = []
    # lexical FSTs
    for pos in morpho:
        anal = morpho[pos].anal(word, guess=False)
        if anal:
            for a in anals:
                anals.append(('lex', pos, a))
    if not anals:
        # guesser FSTs
        for pos in morpho:
            anal = morpho[pos].anal(word, guess=True)
            if anal:
                for a in anals:
                    anals.append(('guess', pos, a))
    return anals
