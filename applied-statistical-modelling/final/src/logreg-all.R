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

formula <- superior_rating ~ 1 + Crisp + Dry + Finish + Firm + Fresh + Fruit + Full + Rich + Round + Soft + Sweet + (-1 + log_price|variety)
library("brms")
bprior <- set_prior("normal(90, 5)", class="Intercept") + prior("normal(0,3)", class="b") + prior("gamma(1,1)", class="sd", group="variety", lb=0)
fit <- brm(
  formula,
  data = df,
  family = bernoulli(),
  prior=bprior,
  chains=8,
  iter=2000,
  cores = 8,
  backend="cmdstanr",
)

fname = "model/logreg-all.rds"
saveRDS(fit, fname)

library(future)

k_fits <- kfold(fit, df, K=10)
k_fits_name <- sub("\\.rds$", ".k-fits.rds", fname)
saveRDS(k_fits, k_fits_name)
