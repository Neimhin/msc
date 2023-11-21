TMP_DIR := tmp

main: tmp/all-source.pdf report.pdf
	pdfunite report.pdf tmp/all-source.pdf a-RobinsonGunningNeimhin-week8.pdf

b-code.zip:
	. src/mk-zip.sh

.PHONY: report.pdf
report.pdf:
	latexmk -pdf report.tex

fig/model_architecture.py.pdf: src/model_architecture.py
	@mkdir -p $(TMP_DIR)
	@enscript -Epython --media=A3 --line-numbers --color --pretty-print -p - $< | tee tmp/output.ps | ps2pdf - $@
	@pdfcrop $@ $@

src/week8.py:
	mkdir -p src
	curl https://www.scss.tcd.ie/Doug.Leith/CSU44061/week8.py | tee $@

TMP_DIR := tmp
SRC_DIR := src
# Define source files
PY_SRC := $(wildcard $(SRC_DIR)/*.py)
SH_SRC := $(wildcard $(SRC_DIR)/*.sh)
SRC := $(PY_SRC) $(SH_SRC)

# Define corresponding PDF files
PDFS := $(patsubst $(SRC_DIR)/%.py,$(TMP_DIR)/%.pdf,$(PY_SRC)) \
        $(patsubst $(SRC_DIR)/%.sh,$(TMP_DIR)/%.pdf,$(SH_SRC))

# Final concatenated PDF file name
FINAL_PDF := $(TMP_DIR)/all-source.pdf

# Target for creating all PDFs
all: $(PDFS) $(FINAL_PDF)

# Rule for concatenating all PDFs into one
$(FINAL_PDF): $(PDFS)
	@pdfunite $^ $@


$(TMP_DIR)/%.pdf: $(SRC_DIR)/%.py
	@mkdir -p $(TMP_DIR)
	@enscript -Epython --color --pretty-print -p - $< | ps2pdf - $@

$(TMP_DIR)/%.pdf: $(SRC_DIR)/%.sh
	@mkdir -p $(TMP_DIR)
	@enscript -Ebash --color --pretty-print -p - $< | ps2pdf - $@

# Target for creating all PDFs
all: $(PDFS)