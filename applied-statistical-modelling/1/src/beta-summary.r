library(MASS)
library(gsl)

a <- as.integer(argv[1])
b <- as.integer(argv[2])
df <- data.frame(a = c(1, 8, 7,  3 ),
                 b = c(1, 8, 13, 29))

beta.mean <- function(a,b) {
  return(a/(a+b))
}
beta.mode <- function(a,b) {
  return((a-1)/(a+b-2))
}
beta.var  <- function(a,b) {
  return((a*b)/((a+b)*(a+b)*(a+b+1)))
}

beta.entropy <- function(a,b) {
  psi_sum <- psi(a) + psi(b)
  entropy <- log(beta(a, b)) - (a - 1) * psi(a) - (b - 1) * psi(b) + (a + b - 2) * psi_sum
  return(entropy)
}

summarise_beta <- function(params){
  a <- params[1]
  b <- params[2]
  cat("a =",a,", b = ", b,"\n")
  conf_interval <- qbeta(c(0.025, 0.975),a,b)
  
  cat("Mean:",     beta.mean(a,b), "\n")
  cat("Mode:",     beta.mode(a,b), "\n")
  cat("Variance:", beta.var(a,b),  "\n")
  # cat("Entropy:", beta.entropy(a,b),  "\n")
  cat("95% Confidence Interval: |", conf_interval[1], "-", conf_interval[2], "| = ", conf_interval[2] - conf_interval[1], "\n\n")
}

for (i in 1:nrow(df)) {
  pair <- df[i,]
  summarise_beta(c(pair$a, pair$b))
}
