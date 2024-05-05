# Read the CSV file
library("ggplot2")
library("future")

df <- read.csv("wine_review.csv")
set.seed(42)
df <- df[sample(1:nrow(df)),]
df$log_price = log(df$price)
df_test <- df[2000:2500,]
df <- df[1:2000,]

formula <- superior_rating ~ 1+(-1+log_price|variety)
library("brms")
bprior <- prior(constant(1), class="sd")
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

saveRDS(fit, "model/logreg-no-covariates.rds")

# # plan(multisession)
# # fits <- kfold(fit, iter=1000, K=5)
# # plan(sequential)h
# 
# # pdf("fig/most-interactions.pdf")
# # plot(fit)
# # conditional_effects(fit)
# # dev.off()
# 
# accuracy <- function(model, data) {
# 	pp <- predict(model, data, type = "response")
# 	predicted_labels <- ifelse(pp > 0.5, 1, 0)[,1]
# 	t <- table(predicted_labels, df$superior_rating)
# 	
# 	# Compare predicted labels to actual labels in the dataset
# 	actual_labels <- df$superior_rating
# 	accuracy <- mean(predicted_labels == actual_labels)
# 	return(accuracy)
# }
# 
# print(paste("Accuracy test: ", accuracy(fit, df_test)))
# print(paste("Accuracy train: ", accuracy(fit, df)))
# 
# # pp <- predict(fit, df_test, type = "response")
# # predicted_labels <- ifelse(pp > 0.5, 1, 0)[,1]
# # t <- table(predicted_labels, df$superior_rating)
# # 
# # # Compare predicted labels to actual labels in the dataset
# # actual_labels <- df$superior_rating
# # accuracy <- mean(predicted_labels == actual_labels)
# # print(actual_labels)
# # accuracy
# # # Print the accuracy
# # print(paste("Accuracy on the test set:", round(accuracy * 100, 2), "%"))
# # ranef(fit)
# # summary(fit)
