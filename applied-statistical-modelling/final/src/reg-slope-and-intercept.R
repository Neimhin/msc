# Read the CSV file
library("ggplot2")
library("future")

options(cmdstanr_write_stan_file_dir = "cmdstanr")

df <- read.csv("wine_review.csv")
set.seed(42)
df <- df[sample(1:nrow(df)),]
df$log_price = log(df$price)
df_test <- df[2000:2500,]
df <- df[1:2000,]

# Crisp + Dry + Finish + Firm + Fresh + Fruit + Full + Rich + Round + Soft + Sweet

formula <- points ~ 1 + Crisp + Dry + Finish + Firm + Fresh + Fruit + Full + Rich + Round + Soft + Sweet + (1+log_price|variety)
library("brms")
bprior <- set_prior("normal(90, 5)", class="Intercept") +
	set_prior("normal(0, 3)", class="b") +
	set_prior("normal(0, 5)", class="sd", group="variety") +
	set_prior("gamma(2, 1)", class="sigma")
fit_all <- brm(
  formula,
  data = df_all,
  family = gaussian(),
  prior=bprior,
  chains=8,
  iter=2000,
  cores = 8,
  backend="cmdstanr",
)
fname_all = "model/reg-slope-and-intercept-all.rds"
saveRDS(fit_all, fname_all)

fit <- brm(
  formula,
  data = df,
  family = gaussian(),
  prior=bprior,
  chains=8,
  iter=2000,
  cores = 8,
  backend="cmdstanr",
)

fname = "model/reg-slope-and-intercept.rds"
saveRDS(fit, fname)
print("model saved")
source("src/describe-fit-reg.R")
describe.fit(fname)
