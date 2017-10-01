#!/usr/bin/env python3

"""
Takes as input a .csv file where refs. are stored, and builds from it a
biblatex-compatible file which can then be used in a LaTeX doc.
"""

import sys                    # For grabbing arguments from the stdin.
import csv                    # For handling csv files.
import re                     # For using regex.
from os import remove as rm   # For removing files if an error occurs.
from os.path import basename  # For stripping the stem from a file.

entry_types = {
    'article'      : ['author', 'title', 'journaltitle', 'year', 'volume', 'number', 'pages', 'doi'],
    'book'         : ['author', 'title', 'year', 'edition', 'publisher', 'location', 'isbn'],
    'conference'   : ['author', 'title', 'booktitle', 'year', 'month', 'location'],
    'electronic'   : ['author', 'title', 'year', 'url'],
    'masterthesis' : ['author', 'title', 'institution', 'year'],
    'phdthesis'    : ['author', 'title', 'institution', 'year']
}

longest = 'journaltitle'


def make_templates(entry_types):  # entry_types is a dict. of lists.
    templates = {}

    for entry_type, fields in entry_types.items():
        indented = [field.ljust(len(longest)) for field in fields]

        templates[entry_type] = '@{}{{{},\n  ' + \
            ' = {{{}}},\n  '.join(indented) + \
            ' = {{{}}}\n}}\n'

    return templates


def main(fname):
    try:
        with open(fname, 'r') as fin, \
             open(fname.replace('.csv', '.bib'), 'w') as fout:

            reader = csv.reader(fin, delimiter=',', quotechar='"')
            templates = make_templates(entry_types)
            regex = ',\n  .{{,{}}} = {{}}'.format(len(longest))

            for row in reader:
                if row[0] in entry_types.keys():
                    template = templates[row[0]]
                    clean_row = list(map(
                        lambda x: x.replace('"', '').replace('&', '\&'), row))
                    formatted = template.format(*clean_row)
                    formatted = re.sub(regex, '', formatted)
                    fout.write(formatted)
                else:
                    raise ValueError('unknown entry type <{}>'.format(row[0]))

    # IndexError is thrown when there are more fields than expected.
    # ValueError is thrown when an unknown reference type is read.
    except (IndexError, ValueError) as err:
        sys.stderr.write('error: {}\n'.format(err.message))
        rm(fout.name)
        return 1

    except FileNotFoundError:
        sys.stderr.write('error: no raw refs file\n')
        return 1

    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('usage: $ python3 {} <fname>\n'.format(
            basename(sys.argv[0])))
        raise SystemExit(1)

    sys.exit(main(sys.argv[1]))
