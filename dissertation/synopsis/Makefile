default: compile

compile:
	pdflatex synopsis.tex

bib:
	bibtex8 -B synopsis.aux

clean:
	$(RM) *.log
	$(RM) *~
	$(RM) *.dvi
	$(RM) text/*.log
	$(RM) text/*~
	$(RM) text/*.dvi


.PHONY: clean compile

