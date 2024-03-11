library(latex2exp) # for TeX
library(ggplot2)
library(gsl) # for psi

generate_beta_density <- function(a, b) {
  p <- seq(0, 1, length.out = 1000)
  density <- dbeta(p, a, b)
  data.frame(p = p, density = density)
}

beta_entropy <- function(p) {
  a <- p[1]
  b <- p[2]
  psi_sum <- psi(a) + psi(b)
  entropy <- log(beta(a, b)) - (a - 1) * psi(a) - (b - 1) * psi(b) + (a + b - 2) * psi_sum
  return(entropy)
}

hypers <- rbind(c(1, 1), c(8, 8), c(7, 13), c(3, 29), c(10, 36), c(9, 41))
beta_entropies <- apply(hypers, 1, beta_entropy)

df_all <- NULL
for (i in 1:nrow(hypers)) {
  df <- generate_beta_density(hypers[i, 1], hypers[i, 2])
  df$group <- paste("a=", hypers[i, 1], ", b=", hypers[i, 2], "",sep="")
  df_all <- rbind(df_all, df)
}

ggplot(df_all, aes(x = p, y = density, color = group)) +
  geom_line() +
  labs(x = TeX("$\\theta$"), y = TeX("$p(\\theta; a, b)$"), color = "Parameters") +
  theme_minimal() +
  theme(legend.position = "top")

ggsave(argv[1])
