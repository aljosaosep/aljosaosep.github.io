DOCNAME=dummy

all: report

.PHONY: clean

report:
	pdflatex ${DOCNAME}.tex
	bibtex ${DOCNAME}.aux
	pdflatex ${DOCNAME}.tex
	pdflatex ${DOCNAME}.tex
	htlatex ${DOCNAME}.tex
	cat ${DOCNAME}.html > ${DOCNAME}.txt
view: report
	open $(DOCNAME).pdf

clean:
	rm *.blg *.bbl *.aux *.log
