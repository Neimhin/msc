fit <- readRDS("model/variety-grouped.rds")

library(ggplot2)

# Extract the ranef data
ranef_data <- as.data.frame(ranef(fit)$variety[,, "Intercept"])

# Create the boxplot using ggplot2
boxplot <- ggplot(ranef_data, aes(x = reorder(rownames(ranef_data), Estimate), y = Estimate)) +
  geom_boxplot(aes(ymin = Q2.5, lower = Q2.5, middle = Estimate, upper = Q97.5, ymax = Q97.5), 
               stat = "identity", fill = "lightblue", color = "blue") +
  coord_flip() +  # Flip the axes for horizontal boxplots
  labs(title = "Variety-Specific Intercepts", 
       x = "Variety", 
       y = "Intercept Estimate") +
  theme_minimal()

# Display the boxplot
print(boxplot)



# Extract the ranef data
ranef_data <- as.data.frame(ranef(fit)$variety[,, "log_price"])

# Create the boxplot using ggplot2
boxplot <- ggplot(ranef_data, aes(x = reorder(rownames(ranef_data), Estimate), y = Estimate)) +
  geom_boxplot(aes(ymin = Q2.5, lower = Q2.5, middle = Estimate, upper = Q97.5, ymax = Q97.5), 
               stat = "identity", fill = "lightblue", color = "blue") +
  coord_flip() +  # Flip the axes for horizontal boxplots
  labs(title = "Variety-Specific Intercepts", 
       x = "Variety", 
       y = "Intercept Estimate") +
  theme_minimal()

# Display the boxplot
print(boxplot)
