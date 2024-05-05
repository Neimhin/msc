# Load the required libraries
library(dplyr)

# Read the CSV file
df <- read.csv("wine_review.csv")
# Convert 'superior_rating' to a factor with meaningful levels
df$superior_rating <- factor(df$superior_rating)

# Create new features
df$log_price <- log(df$price)
df$rich_and_full <- df$Rich & df$Full
df$soft_and_crisp <- df$Soft & df$Crisp
df$not_soft <- !df$Soft
df$not_soft_and_rich <- df$not_soft & df$Rich

df_train <- df[sample(1:2000, 2000),]
df_test <- df[sample(2000:2500, 500),]


# Fit the logistic regression model
model <- glm(
	     points
	     ~ log_price
	     + Soft
	     + Crisp
	     + Full
	     + Rich
	     + rich_and_full
	     + soft_and_crisp
	     # + not_soft_and_rich
     , 
             data = df_train, family = binomial(link="logit"))

# Print the summary of the model
summary(model)

# Use the model to predict probabilities
predicted_points <- predict(model, df_test, type = "response")


# Convert predicted probabilities to predicted class labels
predicted_labels <- ifelse(predicted_points > 90, 1, 0)

# Compare predicted labels to actual labels in the dataset
actual_labels <- df_test$superior_rating
accuracy <- mean(predicted_labels == actual_labels)

# Print the accuracy
print(paste("Accuracy on the test set:", round(accuracy * 100, 2), "%"))

# Create a DataFrame with actual and predicted labels
results_df_test <- data.frame(Actual_Labels = actual_labels, Predicted_Labels = predicted_labels)

# Print the DataFrame
# print(results_df_train)
