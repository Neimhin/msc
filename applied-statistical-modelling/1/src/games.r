library(stats)

# Parameters
alpha <- 3
beta <- 29

df <- data.frame(a = c(10, 9,  3 ),
                 b = c(36, 41, 29))
apply(df, 1, function(row) {
  num_samples <- 10000000
  num_games <- 52
  alpha <- row[1]
  beta <- row[2]
  
  # Simulate Game 1
  theta_samples <- rbeta(num_samples, alpha, beta)
  W_samples <- rbinom(num_samples, num_games, theta_samples)
  game1_return <-  (10 * W_samples) - 100
  
  # Simulate Game 2
  game2_return <- (10 * W_samples^2) - 1000
  
  # Calculate expected return for each game
  expected_return_game1 <- mean(game1_return)
  expected_return_game2 <- mean(game2_return)
  
  cat(paste("a =", row[1], ", b =", row[2]), "\n")
  cat(paste("Expected return for Game 1:", expected_return_game1), "\n")
  cat(paste("Expected return for Game 2:", expected_return_game2),"\n")
  cat("\n")
})
