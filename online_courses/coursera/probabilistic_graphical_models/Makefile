OBJ := main

build: 
	latex $(OBJ)
	makeglossaries $(OBJ)
	latex $(OBJ)
	latex $(OBJ)

.PHONY: clean

#note that a space is needed between {} and \;
clean:
	find . -name 'main.*' ! -name '*.tex' -exec rm -rf {} \;

pdf: 
	pdflatex $(OBJ)

show: 
	xdvi $(OBJ)
