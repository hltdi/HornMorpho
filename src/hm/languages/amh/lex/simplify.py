import glob, os

indir = '.'
outdir = 'new'

def simplify_files():
    lexes = glob.glob(os.path.join(indir, '*.lex'))
    for lex in lexes:
        print('Simplifying', lex)
        inpath = os.path.join(indir, lex)
        outpath = os.path.join(indir, outdir, lex)
        simplify_file(inpath, outpath)

def simplify_file(inpath, outpath):
    with open(inpath, encoding='utf8') as i:
        with open(outpath, 'w', encoding='utf8') as o:
            for line in i:
                if line[0] == '#':
                    continue
                if '^' in line or '`' in line or 'H' in line:
                    if ' ' in line:
                        split_line = line.split()
                        if len(split_line) == 2:
                            if '^' in line or 'H' in line or '`' in line:
                                # skip it
                                pass
                            else:
                                o.write(line)
                        else:
                            alt, root, feats = split_line
                            if '^' in alt or '`' in alt or 'H' in alt:
                                # complicated alternate
                                alt = simplify(alt)
                                root = simplify(root)
                                if feats or alt != root:
                                    o.write('{}   {}   {}\n'.format(alt, root, feats))
                                else:
                                    # drop it
                                    print('Dropping', line.strip())
                            else:
                                # simplified alternate for root; drop it
                                print('Dropping', line.strip())
#                                o.write(line)
                    else:
                        # no alternate, just simplify the root
                        o.write(simplify(line))
                else:
                    o.write(line)

def simplify(text):
    '''Convert alternate consonants to the default.'''
    text = text.replace('^', '')
    # H -> h
    text = text.replace('H', 'h')
    # ` -> '
    text = text.replace('`', "'")
    return text
                         
