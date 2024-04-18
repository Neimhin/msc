all: report-and-code.pdf code.zip
report-and-code.pdf: report.pdf tmp/all-source.pdf
	pdfunite report.pdf tmp/all-source.pdf $@

code.zip: src data fig Makefile run.sh
	zip -r $@ $^

report.pdf: report.lyx
	lyx --export-to pdf4 report.pdf report.lyx

src/cps.py.pdf: src/cps.py
	enscript -M A3 -Epython --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@

SRC_DIR := src
TMP_DIR := tmp
OUTPUT_DIR := output
PYTHON_FILES := $(wildcard $(SRC_DIR)/*.py)
PDF_FILES := $(addprefix $(TMP_DIR)/,$(notdir $(PYTHON_FILES:.py=.pdf)))
tmp/all-source.pdf: $(PDF_FILES)
	@pdfunite $^ $@

$(TMP_DIR)/%.pdf: $(SRC_DIR)/%.py
	@mkdir -p $(TMP_DIR)
	@enscript -M A3 --line-numbers -Epython --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@

best_params: b_mod-N33-M10-it3.json.pdf b-N33-M10-it3.json.pdf a-N99.json.pdf

b_mod-N33-M10-it3.json.pdf: b_mod-N33-M10-it3.json
	enscript -M A3 -Epython --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@
b-N33-M10-it3.json.pdf: b-N33-M10-it3.json
	enscript -M A3 -Epython --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@
a-N99.json.pdf: a-N99.json
	enscript -M A3 -Epython --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@

bii-all: bii-all-data bii/fa.pdf bii/fb.pdf bii/fb_mod.pdf bii/ga.pdf bii/gb.pdf bii/gb_mod.pdf

bii-fig-clean:
	rm bii/fa.pdf bii/fb.pdf bii/fb_mod.pdf bii/ga.pdf bii/gb.pdf bii/gb_mod.pdf

bii/fa.pdf: bii/fa.json
	python src/bii-vis1.py -i $< -o $@ --function f --thin 1 --title 'rnd search a on $$f(x)$$'

bii/fb.pdf: bii/fb.json
	python src/bii-vis1.py -i $< -o $@ --function f --thin 1 --title 'rnd search b on $$f(x)$$'

bii/fb_mod.pdf: bii/fb_mod.json
	python src/bii-vis1.py -i $< -o $@ --function f --thin 1 --title 'rnd search b_mod on $$f(x)$$'

bii/ga.pdf: bii/ga.json
	python src/bii-vis1.py -i $< -o $@ --function g --thin 1 --title 'rnd search a on $$g(x)$$'

bii/gb.pdf: bii/gb.json
	python src/bii-vis1.py -i $< -o $@ --function g --thin 1 --title 'rnd search b on $$g(x)$$'

bii/gb_mod.pdf: bii/gb_mod.json
	python src/bii-vis1.py -i $< -o $@ --function g --thin 1 --title 'rnd search b_mod on $$g(x)$$'

bii-all-data: data/bii-time.json bii/fa.json bii/ga.json bii/fb.json bii/gb.json bii/fb_mod.json bii/gb_mod.json

data/bii-time.json: src/bii-time.py
	python $<

bii/fa.json: data/bii-time.json
	cat data/bii-time.json | jq .f.a[0].stats.it_params > $@

bii/ga.json: data/bii-time.json
	cat data/bii-time.json | jq .g.a[0].stats.it_params > $@ 

bii/fb.json: data/bii-time.json
	cat data/bii-time.json | jq .f.b[0].stats.it_params > $@

bii/gb.json: data/bii-time.json
	cat data/bii-time.json | jq .g.b[0].stats.it_params > $@ 

bii/fb_mod.json: data/bii-time.json
	cat data/bii-time.json | jq .f.b_mod[0].stats.it_params > $@

bii/gb_mod.json: data/bii-time.json
	cat data/bii-time.json | jq .g.b_mod[0].stats.it_params > $@ 
