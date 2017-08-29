TEX       := pdflatex
BIB       := biber

TEXFLAGS  := -halt-on-error -file-line-error

TEXDIR    := chapters
REFDIR    := refs

DISS      := main.pdf
REFS      := abbrvs.tex biblio.bib
TEXSRCS   := $(wildcard *.tex $(TEXDIR)/*.tex)
REFSRCS   := $(wildcard $(REFDIR)/*.csv)

RM        ?= rm
GREP      ?= grep
OPEN      ?= open
PYTHON    ?= python
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

$(REFS): $(REFSRCS)
	@echo 'make: building refs...'
	@$(PYTHON) make-refs.py $(REFDIR)

clean:
	@echo 'make: cleaning...'
	@$(RM) -f $(DISS) $(REFS) *.acn *.acr *.alg *.aux *.bbl *.bcf *.blg
	@$(RM) -f *.log *.out *.pdf *.xml *.toc *.xdy

help:
	@echo 'Targets:'
	@echo ''
	@echo ' all      - Builds all targets marked with [*].'
	@echo ' *diss    - Builds the dissertation in .pdf format.'
	@echo ' *refs    - Builds the abbreviations and bibliography.'
	@echo ' *clean   - Removes all generated files.'
	@echo ' help     - Shows this help message.'
	@echo ' print-%  - Prints the value of variable %.'
	@echo ''
	@echo 'Run "make diss" to build the dissertation if any .tex file in the tree has been'
	@echo 'updated, or "make" or "make all" to build no matter what.'

# For printing the value of a make variable.
print-%:
	@echo '$*=$($*)'

