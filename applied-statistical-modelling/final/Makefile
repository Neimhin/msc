SHELL := /bin/bash

reg: model/reg.k-fits.rds model/reg-slope.k-fits.rds model/reg-slope-and-intercept.k-fits.rds

model/reg.k-fits.rds: model/reg.rds 
	Rscript src/kfold-model.R $<
model/reg.rds: src/reg.R
	Rscript $< | tee $@.log

model/reg-slope.k-fits.rds: model/reg-slope.rds 
	Rscript src/kfold-model.R $<
model/reg-slope.rds: src/reg-slope.R
	Rscript $< | tee $@.log

model/reg-slope-and-intercept.k-fits.rds: model/reg-slope-and-intercept.rds 
	Rscript src/kfold-model.R $<
model/reg-slope-and-intercept.rds: src/reg-slope-and-intercept.R
	Rscript $< | tee $@.log

fig/boxplot-value.pdf: src/boxplot-value.R
	Rscript $<
fig/boxplot-points.pdf: src/boxplot.R src/df.R
	Rscript $<
model/logreg-slope-and-intercept.k-fits.rds: model/logreg-slope-and-intercept.rds
	Rscript src/kfold-model.R $<
model/logreg-slope-and-intercept.rds: src/logreg-slope-and-intercept.R
	Rscript $<
model/logreg-intercept.k-fits.rds: model/logreg-intercept.rds
	Rscript src/kfold-model.R $<
model/logreg-intercept.rds: src/logreg-intercept.R
	Rscript $< $@
model/logreg-all.k-fits.rds: src/kfold-model.R
model/logreg-all.k-fits.rds: model/logreg-all.rds
	Rscript src/kfold-model.R $<
model/logreg-all.rds: src/logreg-all.R
	Rscript $< $@
model/logreg-rich.rds: src/logreg-rich.R
	Rscript $< $@
log/logreg-no-covariates-accuracy.txt: src/logreg-no-covariates-accuracy.R
	Rscript $< | tee -a $@
log/logreg-no-covariates-accuracy.txt: model/logreg-no-covariates.rds
model/logreg-no-covariates.rds: src/logreg-no-covariates.R
	Rscript $< $@
fig/spearman-correlations.pdf: src/spearman-correlations.R
	Rscript $< $@
