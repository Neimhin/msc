source("src/options.R")
data <- data.frame(c(0, 1, 2), c(10, 20, 30), c("a", "b", "c"))
names(data) <- c("x", "y", "c")
print(data)

library(brms)

fit <- brm(
  bf(y ~ c),
  data=data,
  backend="cmdstanr",
)
summary(fit)
ranef(fit)
