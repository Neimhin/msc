TMP_DIR := tmp

fig/model_architecture.py.pdf: src/model_architecture.py
	@mkdir -p $(TMP_DIR)
	@enscript -Epython --media=A3 --line-numbers --color --pretty-print -p - $< | tee tmp/output.ps | ps2pdf - $@
	@pdfcrop $@ $@

src/week8.py:
	mkdir -p src
	curl https://www.scss.tcd.ie/Doug.Leith/CSU44061/week8.py | tee $@

