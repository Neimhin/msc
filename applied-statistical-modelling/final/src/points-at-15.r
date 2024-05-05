fit3 <- readRDS("model/3.rds")

summary(fit3)
library(brms)
ranef(fit3)
