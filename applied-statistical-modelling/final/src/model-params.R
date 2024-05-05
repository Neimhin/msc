
w <- function(v, n) {
	write.csv(v, n, quote=FALSE)
}
extract_model_params <- function(model) {
	library(brms)
	fit <- readRDS(paste0(model,".rds"))
	w(ranef(fit), paste0(model,".ranef.csv"))
	w(fixef(fit), paste0(model,".fixef.csv"))
	w(get_prior(fit), paste0(model,".priors.csv"))
	w(rhat(fit), paste0(model,".rhat.csv"))
}

args = commandArgs(trailingOnly=TRUE)
if(length(args) > 0) {
	model <- args[1]
	extract_model_params(model)
}
