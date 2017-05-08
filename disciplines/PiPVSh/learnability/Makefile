default: compile

compile:
	pdflatex learnability.tex

bib:
	bibtex8 -B learnability.aux

clean:
	$(RM) *.log
	$(RM) *~
	$(RM) *.dvi
	$(RM) text/*.log
	$(RM) text/*~
	$(RM) text/*.dvi


.PHONY: clean compile

