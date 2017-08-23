#!/usr/bin/env python

# Takes as input a .csv file with refs. and turns it into a biblatex-compatible
# .bib file for including in a LaTeX doc.

import sys                    # For handling arguments from the CLI.
import csv                    # For working with csv files.
from os import listdir        # For getting all files in a dir.
from os.path import exists    # For checking if files/dirs. exist.
from os.path import basename  # For stripping the path from a file.
from os.path import splitext  # For stripping the extension from a file.

article=\
'@article{{{nick},\n\
  author       = {{{auth}}},\n\
  title        = {{{titl}}},\n\
  journaltitle = {{{jrnl}}},\n\
  year         = {{{year}}},\n\
  volume       = {{{vol}}},\n\
  number       = {{{num}}},\n\
  pages        = {{{pgs}}},\n\
  doi          = {{{doi}}}\n\
}}\n'

book=\
'@book{{{nick},\n\
  author    = {{{auth}}},\n\
  title     = {{{titl}}},\n\
  address   = {{{addr}}},\n\
  publisher = {{{publ}}},\n\
  year      = {{{year}}}\n\
}}\n'

# Cleans up strings according to the .bib format.
def clean(s):
    return s.replace('"', '').replace('&', '\&')

# Makes the refs. in .bib format from the raw refs. file.
def main(dirname):
    if not exists(dirname):
        sys.stderr.write('error: no raw refs directory\n')
        return 1

    files    = listdir(dirname)
    csvfiles = [f for f in files if f.endswith('.csv')]
    refsfile = open('refs.bib', 'w') # Name the file 'refs.bib'.

    for fname in csvfiles:
        csvfile = open(dirname + '/' + fname, 'r')
        reader  = csv.reader(csvfile, delimiter=',', quotechar='"')
        header  = next(reader) # The first line is the header.

        for row in reader:
            # Articles:
            #   row = [nick, author, title, journal, year, vol, num, pags, doi]
            # Books:
            #   row = [nick, author, title, address, publisher, year]

            if splitext(fname)[0] == 'articles':
                refsfile.write(article.format(
                    nick = clean(row[0]),
                    auth = clean(row[1]),
                    titl = clean(row[2]),
                    jrnl = clean(row[3]),
                    year = clean(row[4]),
                    vol  = clean(row[5]),
                    num  = clean(row[6]),
                    pgs  = clean(row[7]),
                    doi  = clean(row[8])))

            elif splitext(fname)[0] == 'books':
                refsfile.write(book.format(
                    nick = clean(row[0]),
                    auth = clean(row[1]),
                    titl = clean(row[2]),
                    addr = clean(row[3]),
                    publ = clean(row[4]),
                    year = clean(row[5])))

            else:
                sys.stderr.write('error: %s unknown refs file\n' % fname)
                return 1

        csvfile.close()

    refsfile.close()

    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: $ python %s <dirname>\n' % sys.argv[0])
        raise SystemExit(1)

    sys.exit(main(sys.argv[1])); # Get the dir. name from the CLI.

