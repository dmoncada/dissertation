TEX       := pdflatex
BIB       := biber

DISS      := main.pdf
REFS      := refs.bib
TEXDIR    := chapters
TEXSRCS   := $(wildcard *.tex $(TEXDIR)/*.tex)
TEXFLAGS  := -halt-on-error -file-line-error

RM        ?= rm
GREP      ?= grep
OPEN      ?= open
PYTHON    ?= python3
VIEWER    := /Applications/Skim.app

GREPFLAGS := --color=auto -Hn Warning

.PHONY: all diss refs clean help

all: clean refs diss

diss: $(DISS)

refs: $(REFS)

# Why is it necessary to compile so many times?
# See: https://tex.stackexchange.com/questions/62251
$(DISS): $(TEXSRCS)
	@echo 'make: building $@...'
	@$(TEX) $(TEXFLAGS) $(subst .pdf,,$@)
	@$(BIB) $(subst .pdf,,$@)
	@$(TEX) $(TEXFLAGS) $(subst .pdf,,$@)
	@$(TEX) $(TEXFLAGS) $(subst .pdf,,$@)
	@echo ''
	@echo 'make: showing warnings...'
	@$(GREP) $(GREPFLAGS) $(subst .pdf,.log,$@)
	@$(OPEN) -a $(VIEWER) $@

%.bib: %.csv
	@echo 'make: building refs...'
	@$(PYTHON) make-refs.py $<

clean:
	@echo 'make: cleaning...'

	@$(RM) -f $(DISS) $(REFS) *.aux *.bbl *.bcf *.bib *.blg *.fdb_latexmk *.fls *.log *.out *.pdf *.synctex.gz *.toc
	@$(RM) -f *.xml

help:
	@echo 'Targets:'
	@echo ''
	@echo ' all      - Builds all targets marked with [*].'
	@echo ' *diss    - Builds the dissertation in .pdf format.'
	@echo ' *refs    - Builds the bibliography.'
	@echo ' *clean   - Removes all generated files.'
	@echo ' help     - Shows this help message.'
	@echo ' print-%  - Prints the value of variable %.'
	@echo ''
	@echo 'Run "make diss" to build the dissertation if any .tex file in the tree has been'
	@echo 'updated, or "make" or "make all" to build no matter what.'

print-%:
	@echo '$*=$($*)'
