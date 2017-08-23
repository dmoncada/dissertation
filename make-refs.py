#!/usr/bin/env python

"""
Takes as input a dir. where (possibly many) .csv files with refs. are stored,
and merges them into a biblatex-compatible .bib file for including in a LaTeX
doc.

The .csv files should be named according to the refs. they contain, e.g. a .csv
containing articles refs. should be 'articles.csv', etc. Currently supported
file names include: 'articles.csv' and 'books.csv'. More to come.
"""

import sys                    # For handling arguments from the CLI.
import csv                    # For handling csv files.
from os import listdir        # For listing all files in a dir.
from os.path import exists    # For checking if files/dirs. exist.
from os.path import basename  # For stripping the path from a file.
from os.path import splitext  # For stripping the extension from a file.

article=\
'@article{{{},\n\
  author       = {{{}}},\n\
  title        = {{{}}},\n\
  journaltitle = {{{}}},\n\
  year         = {{{}}},\n\
  volume       = {{{}}},\n\
  number       = {{{}}},\n\
  pages        = {{{}}},\n\
  doi          = {{{}}}\n\
}}\n'

book=\
'@book{{{},\n\
  author    = {{{}}},\n\
  title     = {{{}}},\n\
  address   = {{{}}},\n\
  publisher = {{{}}},\n\
  year      = {{{}}}\n\
}}\n'

# Cleans up strings according to the .bib format.
def clean(ls):
    return [s.replace('"', '').replace('&', '\&') for s in ls]

# Makes the refs. in .bib format from the raw refs. file.
def main(dirname):
    if not exists(dirname):
        sys.stderr.write('error: no raw refs directory\n')
        return 1

    csvfiles = [f for f in listdir(dirname) if f.endswith('.csv')]

    with open('refs.bib', 'w') as refsfile:
        for fname in csvfiles:
            with open(dirname + '/' + fname, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"')
                header = next(reader) # Get rid of the header.

                for row in reader:
                    stem = splitext(fname)[0] # The file name without extension.

                    # Articles:
                    #  row = [label, author, title, journal, year, vol, num, pags, doi]
                    # Books:
                    #  row = [label, author, title, address, publisher, year]

                    if stem == 'articles':
                        refsfile.write(article.format(*clean(row)))
                    elif stem == 'books':
                        refsfile.write(book.format(*clean(row)))
                    else:
                        sys.stderr.write('error: %s unknown refs file\n' % fname)
                        return 1

    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: $ python %s <dirname>\n' % sys.argv[0])
        raise SystemExit(1)

    sys.exit(main(sys.argv[1])); # Get the dir. name from the CLI.

