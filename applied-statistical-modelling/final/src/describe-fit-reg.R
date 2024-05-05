accuracy <- function(model, data, threshold=90) {
	pp <- predict(model, data, type = "response")
	predicted_labels <- ifelse(pp >= threshold, 1, 0)[,1]
	actual_labels <- data$superior_rating
	accuracy <- mean(predicted_labels == actual_labels)
	return(accuracy)
}

source("src/df.R")

describe.fit <- function(model, threshold=90) {
	fit <- readRDS(model)
	summary(fit)
	library(brms)
	ranef(fit)
	print(paste("Accuracy test: ", accuracy(fit, df_test, threshold=threshold)))
	print(paste("Accuracy train: ", accuracy(fit, df, threshold=threshold)))
}

args <- commandArgs(trailingOnly=TRUE)
if(length(args) > 0) {
	describe.fit(args[1])
}
