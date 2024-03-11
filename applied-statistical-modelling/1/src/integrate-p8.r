library(stats)

# Define the functions for p(W >= 8 | theta) and p(theta)
p_W_given_theta <- function(theta) {
  1 - pbinom(7, 52, theta)
}

p_theta <- function(theta) {
  dbeta(theta, 3, 29)
}

# Compute the joint probability by integrating the product of the two functions
joint_probability <- function(theta) {
  p_W_given_theta(theta) * p_theta(theta)
}

# Integrate the joint probability function numerically
result <- integrate(joint_probability, lower = 0, upper = 1)

# The result$value contains the estimated probability
print(paste("Estimated probability:", result$value))
