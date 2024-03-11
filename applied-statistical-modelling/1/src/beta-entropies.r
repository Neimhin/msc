library(gsl)
library(ggplot2)

beta_entropy <- function(params) {
  a <- params[1]
  b <- params[2]
  
  if (a <= 0 || b <= 0) {
    stop("Parameters 'a' and 'b' must be greater than zero.")
  }
  
  psi_sum <- psi(a) + psi(b)
  entropy <- log(beta(a, b)) - (a - 1) * psi(a) - (b - 1) * psi(b) + (a + b - 2) * psi_sum
  
  cat(a,b,a+b,entropy,"\n")
  return(entropy)
}

pairs <- expand.grid(a= 1:10, b=1:10)
pairs$entropy <- apply(pairs, 1, beta_entropy)

ggplot(pairs, aes(x = a + b, y = entropy)) +
  geom_point() +
  labs(x = "a + b", y = "Entropy") +
  ggtitle("Entropy of Beta Distribution vs. a + b")

ggsave(argv[1])
