#!/usr/bin/env python

"""
Takes as input a dir. where (possibly many) .csv files with refs. are stored,
and builds from them both acro- and biblatex-compatible files which can then be
used in a LaTeX doc.
"""

import sys                    # For handling arguments from the CLI.
import csv                    # For handling csv files.
from os import listdir        # For listing all files in a dir.
from os.path import isdir     # For checking if dirs. exist.
from os.path import exists    # For checking if files exist.
from os.path import basename  # For stripping the path from a file.
from os.path import splitext  # For stripping the extension from a file.

abbrv_style = """\
% Define a new list style...
\\newlist{acronyms}{description}{1}
\\setlist[acronyms]{format=\\textnormal,labelindent=7.5mm,labelwidth=25mm,noitemsep}

% ...and attach it to 'acrostyle'.
\\DeclareAcroListStyle{acrostyle}{list}{list=acronyms}

% Set the style for the list and the format for the acronyms' first expansion.
\\acsetup{list-style=acrostyle,first-long-format=\\em\\lowercase}

% Acronyms
"""

acronym = '\\DeclareAcronym{{{}}}{{short={},long={}}}'

article = """\
@article{{{},
  author       = {{{}}},
  title        = {{{}}},
  journaltitle = {{{}}},
  year         = {{{}}},
  volume       = {{{}}},
  number       = {{{}}},
  pages        = {{{}}},
  doi          = {{{}}}
}}
"""

book = """\
@book{{{},
  author    = {{{}}},
  title     = {{{}}},
  address   = {{{}}},
  publisher = {{{}}},
  year      = {{{}}}
}}
"""

# Cleans up strings according to the .bib format.
def clean(ls):
    return [s.replace('"', '').replace('&', '\&') for s in ls]

def make_abbrvs(dirname):
    fname = dirname + '/abbrvs.csv'

    if not exists(fname):
        sys.stderr.write('error: no raw file for abbreviations\n')
        return 1

    fin    = open(fname, 'r')
    fout   = open(basename(fname).replace('.csv', '.tex'), 'w')
    reader = csv.reader(fin)
    header = next(reader) # Get rid of the header.

    # row = [label, short, long]

    fout.write(abbrv_style +
               '\n'.join([acronym.format(*row) for row in reader]))

    fin.close()
    fout.close()

    return 0

# Makes the refs. in .bib format from the raw refs. file.
def make_biblio(dirname):
    files = [f for f in listdir(dirname) if f.endswith('.csv') and
             ('articles' in f or 'books' in f)] # Keep it simple.

    if not files:
        sys.stderr.write('error: no raw files for bibliography\n')
        return 1

    fout = open('biblio.bib', 'w')

    for fname in files:
        fin    = open(dirname + '/' + fname, 'r')
        reader = csv.reader(fin, delimiter=',', quotechar='"')
        header = next(reader)

        for row in reader:
            stem = splitext(fname)[0] # The file name without extension.

            # Articles:
            #  row = [label, author, title, journal, year, vol, num, pags, doi]
            # Books:
            #  row = [label, author, title, address, publisher, year]

            if stem == 'articles':
                fout.write(article.format(*clean(row)))
            elif stem == 'books':
                fout.write(book.format(*clean(row)))

        fin.close()
    fout.close()

    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: $ python %s <dirname>\n' % sys.argv[0])
        raise SystemExit(1)

    dirname = sys.argv[1]

    if not isdir(dirname):
        sys.stderr.write('error: no raw refs directory\n')
        raise SystemExit(1)

    sys.exit(make_abbrvs(dirname) or make_biblio(dirname))

