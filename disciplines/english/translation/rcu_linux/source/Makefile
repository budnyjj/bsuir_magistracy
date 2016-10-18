TARGET = paper
DEPS = intro.tex background.tex api_usage.tex tree_rcu.tex api_impl.tex callback.tex \
       data_structure.tex quiescent_state_detection.tex grace_period_detection.tex \
       running_example.tex modeling.tex experiments.tex bug_cases.tex cbmc.tex \
       results_cbmc.tex results_run.tex related_work.tex concl.tex barchart_*.tex \

CLASSFILE = 
BIBFILE = paper.bib

SOURCE_FILE = $(TARGET).tex

LATEX = pdflatex
BIBTEX = bibtex

all: $(TARGET).pdf

$(CLASSFILE):

$(BIBFILE):

$(TARGET).pdf: $(SOURCE_FILE) $(DEPS) $(CLASSFILE) $(BIBFILE)
	$(LATEX) $(SOURCE_FILE)
	$(BIBTEX) $(TARGET)
	while ( \
		$(LATEX) $(TARGET) ; \
		grep "Rerun to get" $(TARGET).log > /dev/null \
	) do true ; done

clean:
	rm -f $(TARGET).aux $(TARGET).bbl $(TARGET).blg $(TARGET).log 

allclean: clean
	rm -f $(TARGET).pdf

