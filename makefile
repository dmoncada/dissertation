TEX      = pdflatex
GLS      = makeglossaries
BIB      = biber

TEXFLAGS = -halt-on-error -file-line-error

TEXDIR   = chapters
REFDIR   = refs

DISS     = main.pdf
REFS     = refs.bib
TEXSRCS  = $(wildcard *.tex $(TEXDIR)/*.tex)
REFSRCS  = $(wildcard $(REFDIR)/*.csv)

RM      ?= rm
OPEN    ?= open
PYTHON  ?= python
VIEWER   = /Applications/Skim.app

.PHONY: all diss refs clean help

all: clean refs diss

diss: $(DISS)

refs: $(REFS)

# Why is it necessary to compile so many times?
# See: https://tex.stackexchange.com/questions/62251
$(DISS): $(TEXSRCS)
	@echo 'make: building $@...'
	$(TEX) $(TEXFLAGS) $(subst .pdf,,$@)
	$(GLS) $(subst .pdf,,$@) # Glossary.
	$(BIB) $(subst .pdf,,$@) # Bibliography.
	$(TEX) $(TEXFLAGS) $(subst .pdf,,$@)
	$(TEX) $(TEXFLAGS) $(subst .pdf,,$@)
	$(OPEN) -a $(VIEWER) $@

$(REFS): $(REFSRCS)
	@echo 'make: building $@...'
	@$(PYTHON) make-refs.py $(REFDIR)

clean:
	@echo 'make: cleaning...'
	@$(RM) -f *.acn *.acr *.alg *.aux *.bib *.bbl *.bcf *.blg *.glg *.glo
	@$(RM) -f *.gls *.glsdefs *.ist *.lof *.log *.lot *.out *.pdf *.xml *.toc

help:
	@echo 'Targets:'
	@echo ''
	@echo ' all      - Builds all targets marked with [*].'
	@echo ' *diss    - Builds the dissertation in .pdf format.'
	@echo ' *refs    - Builds the references file in .bib format.'
	@echo ' *clean   - Removes all generated files.'
	@echo ' help     - Shows this help message.'
	@echo ' print-%  - Prints the value of variable %.'
	@echo ''
	@echo 'Run "make diss" to build the dissertation if any .tex file in the tree has been'
	@echo 'updated, or "make" or "make all" to build no matter what.'

# For printing the value of a make variable.
print-%:
	@echo "$*=$($*)"

