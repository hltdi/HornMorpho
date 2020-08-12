import glob, os

indir = '.'
outdir = 'new'

def simplify_files():
    cass = glob.glob(os.path.join(indir, '*.cas'))
    for cas in cass:
        print('SIMPLIFYING', cas)
        inpath = os.path.join(indir, cas)
        outpath = os.path.join(indir, outdir, cas)
        simplify_file(inpath, outpath)

def simplify_file(inpath, outpath):
    with open(inpath, encoding='utf8') as i:
        with open(outpath, 'w', encoding='utf8') as o:
            for line in i:
                if '~X' in line:
                    # only characters that are being eliminated
#                    print('Skipping', line.strip())
                    pass
                elif '^' in line or '`' in line or 'H' in line:
                    o.write(simplify(line))
                else:
                    o.write(line)

def simplify(text):
    '''Get rid of ^h, ^s, ^S, H, ` in character lists.'''
#    print('Converting', text)
    text = text.replace('^hW, ', '')
    text = text.replace(', ^hW', '')
    text = text.replace(', ^sW', '')
    text = text.replace(', ^SW', '')
    text = text.replace(', KW', '')
    text = text.replace(', HW', '')
    text = text.replace(', H', '')
    text = text.replace(', K', '')
    text = text.replace(', `', '')
    text = text.replace(', ^h', '')
    text = text.replace(', ^s', '')
    text = text.replace(', ^S', '')
#    print('Converted', text.strip())
    return text
                         
