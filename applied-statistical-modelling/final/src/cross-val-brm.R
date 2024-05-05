
library("brms")
library("cmdstanr")

# Read the CSV file
df <- read.csv("wine_review.csv")
df$superior_rating <- as.factor(df$superior_rating)
df$log_price <- log(df$price)
df$points = df$points - 90

# # Define the list of variable names
# variable_names <- c("Crisp", "Dry", "Finish", "Firm", "Fresh", 
#                     "Fruit", "Full", "Rich", "Round", "Soft", "Sweet", "superior_rating", "variety")
# 
# # Loop through each variable name and convert it to a factor
# for (var_name in variable_names) {
#   df[[var_name]] <- as.factor(df[[var_name]])
# }


# Function to find breakpoints for quintiles
find_breakpoints_quintiles <- function(data) {
  breaks <- quantile(data$price, probs = seq(0, 1, by = 0.2))
  return(breaks)
}

# Find breakpoints for quintiles
breaks <- find_breakpoints_quintiles(df)

generate_labels <- function(breaks) {
  labels <- character(length(breaks) - 1)
  for (i in 1:(length(breaks) - 1)) {
    if (i == length(breaks) - 1) {
      labels[i] <- paste0(breaks[i], "<p")
    } else {
      labels[i] <- paste0(breaks[i], "<p<=", breaks[i + 1])
    }
  }
  return(labels)
}

# Generate labels for the factors
labels <- generate_labels(breaks)

# Create factors based on the ranges
price_factors <- cut(df$price, breaks = breaks, labels = labels, include.lowest = TRUE)

# If you want it as a column in your dataframe, you can do this:
df$price_factor <- price_factors

df$log_price <- log(df$price)
df$rich_and_full <- df$Rich & df$Full
df$soft_and_crisp <- df$Soft & df$Crisp
df$not_soft <- !df$Soft
df$soft_and_rich <- df$Soft & df$Rich
df$Rich <- as.factor(df$Rich)
df$Soft <- as.factor(df$Soft)
df$Full <- as.factor(df$Full)
df$Crisp <- as.factor(df$Crisp)
df$soft_and_crisp <- as.factor(df$soft_and_crisp)
df$rich_and_full <- as.factor(df$rich_and_full)


# Plot the mosaic plot
mosaicplot(table(df$price_factor, df$superior_rating), col=c(2,3), main = "Wine Reviews")

df_test <- df[2000:2500,]
df <- df[1:2000,]


sample_sizes <- table(df$price_factor)

# Print sample size for each factor level
print(sample_sizes)


formula <-  points ~ Soft + Crisp + Full + Rich + rich_and_full + soft_and_crisp  + (1 + log_price|variety)


stan_code <- make_stancode(formula, data=df) #, family=bernoulli(), prior=prior(normal(0,10),class="b"))
print(stan_code)

fit <- brm(
  formula,
  data = df,
  backend="cmdstanr",
  # family = gaussian(),
  # prior = prior(normal(0, 10), class = b),
  prior = c(
    set_prior("normal(0,3)", class="b")
  ),
  cores = 8,
)
summary(fit)
# 
# library(future)
# plan(multisession, workers=8)
# kfold_fits <- kfold(fit, K = 5)
# kfold_fits$predictions[[1]]


predicted_points = predict(fit, df_test)
predicted_superior = predicted_points >= 0
mae <- mean(abs(predicted_points - df_test$points))
mae
accuracy <- mean(as.numeric(predicted_superior) == df_test$superior_rating)
accuracy
stan_code
pdf("fig/hierarchical-model-variety.pdf")
plot(fit)
dev.off()

ranef(fit)

saveRDS(fit, file="model/variety-grouped.rds")

summary(fit)
