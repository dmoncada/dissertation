#!/usr/bin/env python

"""Takes as input a .csv file where refs. are stored, and builds from it a
biblatex-compatible file which can then be used in a LaTeX doc."""

import sys                  # For handling arguments from the CLI.
import csv                  # For handling csv files.
import re                   # For using regex.
from os.path import exists  # For checking if files exist.
from os import remove as rm # For removing files if an error occurred.

entry_types = {
    'article'      : ['author', 'title', 'journaltitle', 'year', 'volume', 'number', 'pages', 'doi'],
    'book'         : ['author', 'title', 'year', 'edition', 'publisher', 'location', 'isbn'],
    'conference'   : ['author', 'title', 'booktitle', 'year', 'month', 'location'],
    'electronic'   : ['author', 'title', 'year', 'url'],
    'masterthesis' : ['author', 'title', 'institution', 'year'],
    'phdthesis'    : ['author', 'title', 'institution', 'year']
}

longest = 'journaltitle'

def make_templs(types): # types is a dict. of lists.
    templs = {}

    for _type, fields in types.iteritems():
        indented = [field.ljust(len(longest)) for field in fields]

        templs[_type] = '@{}{{{},\n  ' + \
                        ' = {{{}}},\n  '.join(indented) + \
                        ' = {{{}}}\n}}\n'

    return templs

# Removes chars. that might bother biber.
def clean(fields):
    return [field.replace('"', '').replace('&', '\&') for field in fields]

def main(fname):
    try:
        with open(fname, 'r') as fin, \
             open(fname.replace('.csv', '.bib'), 'w') as fout:

            reader = csv.reader(fin, delimiter=',', quotechar='"')
            templs = make_templs(entry_types)

            for row in reader:
                if row[0] in entry_types.keys():
                    templ = templs[row[0]]
                    fmttd = templ.format(*clean(row))
                    fmttd = re.sub(',\n  .{,%i} = {}' % len(longest), '', fmttd)
                    fout.write(fmttd)
                else:
                    raise ValueError('unknown entry type \'%s\'' % row[0])

    # IndexError is thrown when there are more fields than expected.
    except (IndexError, ValueError) as err:
        sys.stderr.write('error: ' + err.message + '\n')
        rm(fout.name)
        return 1

    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: $ python %s <fname>\n' % sys.argv[0])
        raise SystemExit(1)

    fname = sys.argv[1]

    if not exists(fname):
        sys.stderr.write('error: no raw refs file\n')
        raise SystemExit(1)

    sys.exit(main(fname))

