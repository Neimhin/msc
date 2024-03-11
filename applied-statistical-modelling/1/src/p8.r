df <- data.frame(a = c(3 , 10, 9),
                 b = c(29, 36, 41))
library(ggplot2)
num_samples <- 10000000
monte_carlo_p8 <- function(alpha, beta) {
    theta_samples <- rbeta(num_samples, alpha, beta)
    W_samples <- rbinom(num_samples, 52, theta_samples)
    probability <- mean(W_samples >= 8)
    cat("Estimated probability:", probability,"\n")
    cat("Num samples:", num_samples, "\n")
}

for (i in 1:nrow(df)) {
  pair <- df[i,]
  monte_carlo_p8(pair$a, pair$b)
}

alpha <- 3
beta <- 29
theta_samples <- rbeta(num_samples, alpha, beta)
W_samples <- rbinom(num_samples, 52, theta_samples)
probability <- mean(W_samples >= 8)
cat("Estimated probability:", probability,"\n")
cat("Num samples:", num_samples, "\n")
df <- data.frame(W=W_samples)

ggplot(df, aes(x = W)) +
  geom_bar(aes(y = ..count.. / sum(..count..)), 
           fill = "skyblue", color = "black") +
  labs(title = "PMF of W_samples",
       x = "Number of Wins (W)",
       y = "Probability") +
  theme_minimal()

ggsave(argv[1])
