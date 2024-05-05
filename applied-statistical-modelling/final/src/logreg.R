# Read the CSV file
df <- read.csv("wine_review.csv")
df$superior_rating <- as.factor(df$superior_rating)
df$log_price = log(df$price)

library("brms")

formula <- bf(points ~ 1 + Crisp + Dry + Finish + Firm + Fresh + Fruit + Full + Rich + Round + Soft + Sweet + log_price + variety,
	      sigma ~ variety)

fit <- brm(
  formula,
  data = df,
  family = gaussian(),
  # prior = prior(normal(0, 10), class = b),
  chains=4,
  iter=2000,
  cores = 8,
  backend="cmdstanr",
)

library(future)
plan(multisession)
fits <- kfold(fit, K=5)
plan(sequential)h

pdf("fig/most-interactions.pdf")
plot(fit)
conditional_effects(fit)
dev.off()

# saveRDS(fit, file="fit/superior_rating-sim-.plus(1|price_factor).rds")
# Use the fitted model to predict probabilities
pp <- predict(fit, type = "response")
# Convert predicted probabilities to predicted class labels
predicted_labels <- ifelse(pp > 0.5, 1, 0)[,1]
t <- table(predicted_labels, df$superior_rating)

# Compare predicted labels to actual labels in the dataset
actual_labels <- df$superior_rating
accuracy <- mean(predicted_labels == actual_labels)
print(actual_labels)
accuracy
# Print the accuracy
print(paste("Accuracy on the training set:", round(accuracy * 100, 2), "%"))
ranef(fit)
summary(fit)
