library(gsl)
library(ggplot2)

beta.var  <- function(pair) {
  a <- pair[1]
  b <- pair[2]
  return((a*b)/((a+b)*(a+b)*(a+b+1)))
}

pairs <- expand.grid(a= 1:10, b=1:10)
pairs$entropy <- apply(pairs, 1, beta.var)

ggplot(pairs, aes(x = a + b, y = entropy)) +
  geom_point() +
  labs(x = "a + b", y = "Variance") +
  ggtitle("Variance of Beta Distribution vs. a + b")

ggsave(argv[1])
