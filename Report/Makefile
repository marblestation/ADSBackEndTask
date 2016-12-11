
Report.pdf: Report.tex References.bib
	pdflatex Report.tex 
	bibtex Report.aux 
	pdflatex Report.tex 
	pdflatex Report.tex 
	rm -f Report.log
	rm -f Report.aux
	rm -f Report.bbl
	rm -f Report.blg
	rm -f Report.out
	rm -f Report.toc

clean:
	rm -f Report.pdf
	rm -f Report.log
	rm -f Report.aux
	rm -f Report.bbl
	rm -f Report.blg
	rm -f Report.out
	rm -f Report.toc

