fit <- readRDS("mod.rds")

library(brms)
write.csv(ranef(fit), "ranef.csv")
write.csv(fixef(fit), "fixef.csv")
write.csv(get_prior(fit), "priors.csv")
