library("ggplot2")
library("corrplot")

data <- read.csv("wine_review.csv")
data$log_price <- scale(log(data$price))
data$notSoft <- !data$Soft
data$notCrisp <- !data$Crisp
data$notFinish <- !data$Finish
data$rich.x.notSoft <- data$Rich & data$notSoft
data$Rich.x.Full <- data$Rich & data$Full
data$Rich.x.log_price <- data$Rich * data$log_price
data$Full.x.notSoft <- data$Full & data$notSoft

use <-  c("points",
          "log_price",
          "Full",
          "Rich",
          "Soft",
          "Crisp",
          "Round",
          "Fruit",
          "Sweet",
          "Finish",
          "Dry",
          "notSoft",
          "notCrisp", 
          "notFinish",
          "rich.x.notSoft",
          "Rich.x.Full",
          "Rich.x.log_price",
          "Full.x.notSoft"
          )
sub <- data[,use]
library(psych)

correlations <- corr.test(sub, method='pearson')$r[,"points"]

# Create a data frame for plotting
correlation_df <- data.frame(variable = names(correlations), correlation = correlations)
correlation_df <- correlation_df[order(correlation_df$correlation, decreasing = TRUE), ]
correlation_df$variable <- factor(correlation_df$variable, levels = correlation_df$variable)

# Plot Spearman's correlation coefficients
pdf("fig/spearman-correlations.pdf")
p <- ggplot(correlation_df, aes(x = variable, y = correlation)) +
  geom_point(fill = "white", color = "black") +
  # geom_text(aes(label = round(correlation, 2)), size = 3) +
  labs(title = "Spearman's Correlation to data$points", x = NULL, y = "Spearman's Correlation") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
print(p)
dev.off()
