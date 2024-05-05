# Read the CSV file
source("src/df.R")
source("src/options.R")
library("ggplot2")
library("future")
# Crisp + Dry + Finish + Firm + Fresh + Fruit + Full + Rich + Round + Soft + Sweet
formula <- points ~ 1 + log_price + Crisp + Full + Rich + Soft + (1+log_price|variety)
library("brms")
bprior <- set_prior("normal(80, 10)", class="Intercept") +
	set_prior("normal(0, 5)", class="b")
	set_prior("gamma(1, 1)", class="sd", group="variety") +
	set_prior("gamma(1, 1)", class="sigma")
fit_all <- brm(
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
default_prior(fit_all)
summary(fit_all)
ranef(fit_all)
fname_all = "model/reg-slope-and-intercept-all.rds"
saveRDS(fit_all, fname_all)
source("src/describe-fit-reg.R")
print(paste("train accuracy:", accuracy(fit_all, df_all)))
