default: compile

compile:
	pdflatex hybrid.tex

bib:
	bibtex8 -B hybrid.aux

clean:
	$(RM) *.log
	$(RM) *~
	$(RM) *.dvi
	$(RM) text/*.log
	$(RM) text/*~
	$(RM) text/*.dvi


.PHONY: clean compile

