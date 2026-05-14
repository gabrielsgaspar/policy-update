.PHONY: pdf watch clean

pdf:
	latexmk -pdf main.tex

watch:
	latexmk -pvc -pdf main.tex

clean:
	latexmk -C main.tex
	rm -rf build
