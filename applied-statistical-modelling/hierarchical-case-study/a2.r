df2 <- read.csv("simpsons.csv")
dim(df2)
df2$SeasonF <- factor(df2$Season)
nlevels(df2$SeasonF)

library("ggplot2")
ggplot(df2) + geom_boxplot(aes(x = reorder(SeasonF, Rating, median), 
                               Rating, 
                               fill = reorder(SeasonF, Rating, median)), 
                           show.legend=FALSE) + 
  labs(x = "Season", y = "Rating") + 
  theme(axis.text.x = element_text(size = 7.5)) + coord_flip()

ggplot(df2, aes(x = Rating)) +
  geom_histogram(binwidth=0.2) +
  labs(title = "Histogram of Ratings",
       x="Rating",
       y="Frequency")

n <-10
# Splitting the data into two groups based on the season variable
season_group1 <- subset(df2, Season < n)
season_group2 <- subset(df2, Season >= n)

n_minus_1 <- n - 1

# Histogram for season_group1
ggplot(season_group1, aes(x = Rating)) +
  geom_histogram(binwidth = 0.2, fill = "blue", color = "black") +
  labs(title = sprintf("Histogram of Ratings - Seasons 1 to %d", n_minus_1),
       x = "Rating",
       y = "Frequency")

# Histogram for season_group2
ggplot(season_group2, aes(x = Rating)) +
  geom_histogram(binwidth = 0.2, fill = "red", color = "black") +
  labs(title = sprintf("Histogram of Ratings - Seasons %d onwards", n),
       x = "Rating",
       y = "Frequency")

season_means <- tapply(df2$Rating, df2$SeasonF, mean)
print(season_means)
tab_season <- table(df2$SeasonF)
fivenum(tab_season)

# Not interesting here
df_est <- data.frame(size = as.numeric(tab_season), ybar=season_means)
rownames(df_est) <- names(tab_season)
ggplot(df_est) + geom_point(aes(x=size, y=ybar))

library("rstan")
options(mc.cores = parallel::detectCores())
N = nrow(df2)
rating <- df2$Rating
school_ind <- df2$Season
K <- max(school_ind)
dat_stan <- list(
  N = N,
  K = K,
  rating = rating,
  season_ind = season_ind,
  mu_0 = 5,
  sd_0 = 2,
  a_0 = 1,
  b_0 = 400,
  alpha_0 = 1,
  beta_0 = 400
  )

renv::status()
fit_stan <- stan(file = 'simpsons.stan', data = dat_stan)
pairs(fit_stan, pars = c("mu", "tau_b", "tau_w"))
