# Read the CSV file
df <- read.csv("wine_review.csv")
df$superior_rating <- as.factor(df$superior_rating)
df$log_price = log(df$price)

library("brms")

formula <- bf(  points ~ 1 + Crisp + Dry + Finish + Firm + Fresh + Fruit + Full + Rich + Round + Soft + Sweet + log_price + variety,
	  	sigma ~ variety)
fit <- brm(
  formula,
  data = df,
  family = gaussian(),
  chains=4,
  iter=2000,
  cores = 8,
  backend="cmdstanr",
)
saveRDS(fit, "model/gaussian-sigma.R")
