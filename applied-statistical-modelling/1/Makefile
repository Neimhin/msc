report-and-code.pdf: report.pdf all-sources.pdf
	pdfunite $^ $@

report.pdf: report.lyx fig/q4.pdf fig/q5.pdf fig/betas.pdf fig/beta-summaries.pdf
	lyx --export-to pdf4 report.pdf report.lyx

fig/q4.pdf: fig/q4.txt
	enscript -M A3 --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@

fig/q4.txt: src/p8.r
	r $< fig/q8.pdf | tee $@

fig/q5.pdf: fig/q5.txt
	enscript -M A3 --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@

fig/q5.txt: src/games.r
	r src/games.r | tee $@

fig/betas.pdf: src/betas.r
	r src/betas.r $@

a1.pdf: a1.md
	Rscript render.r

fig/beta-summaries.txt: src/beta-summary.r
	r $< > $@

fig/beta-summaries.pdf: fig/beta-summaries.txt
	enscript -M A3 --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@

fig/beta-sum-vs-var.pdf: src/beta-variances.r
	r $< $@

fig/beta-8-8.pdf: beta_dists
fig/beta-7-13.pdf: beta_dists
fig/beta-16-16.pdf: beta_dists

src/p8.r.pdf: src/p8.r
	enscript -M A3 -E r --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@
src/beta-entropies.r.pdf: src/beta-entropies.r
	enscript -M A3 -E r --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@
src/betas.r.pdf: src/betas.r
	enscript -M A3 -E r --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@
src/beta-summary.r.pdf: src/beta-summary.r
	enscript -M A3 -E r --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@
src/beta-variances.r.pdf: src/beta-variances.r
	enscript -M A3 -E r --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@
src/games.r.pdf: src/games.r
	enscript -M A3 -E r --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@
src/integrate-p8.r.pdf: src/integrate-p8.r
	enscript -M A3 -E r --line-numbers --color --pretty-print -p - $< | ps2pdf - - | pdfcrop - $@
all-sources.pdf: src/p8.r.pdf src/beta-entropies.r.pdf src/betas.r.pdf src/beta-summary.r.pdf src/beta-variances.r.pdf src/games.r.pdf src/integrate-p8.r.pdf 
	pdfunite $^ $@
