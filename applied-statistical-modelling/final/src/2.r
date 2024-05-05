# Read the CSV file
source("src/df.R")
source("src/options.R")
library("ggplot2")
library("future")
# Crisp + Dry + Finish + Firm + Fresh + Fruit + Full + Rich + Round + Soft + Sweet
formula <- points ~ 1 + log_price + Crisp + Full + Rich + Soft + (-1+log_price|variety)
library("brms")
bprior <- set_prior("normal(80, 10)", class="Intercept") +
	set_prior("normal(0, 5)", class="b") +
	set_prior("gamma(2, 1)", class="sd", group="variety") +
	set_prior("gamma(2, 1)", class="sigma")
fit <- brm(
  formula,
  data = df_all,
  family = gaussian(),
  prior=bprior,
  chains=4,
  iter=2000,
  cores = 4,
  backend="cmdstanr",
  threads = threading(2)
)
model = "model/2"
fname_all = paste0(model,".rds")
saveRDS(fit, fname_all)
source("src/describe-fit-reg.R")
print(paste("train accuracy:", accuracy(fit, df_all)))
source("src/model-params.R")
extract_model_params(model)
k_fits <- kfold(fit, K=10, save_fits=TRUE)
saveRDS(k_fits,paste0(model, ".k-fits.rds"))
