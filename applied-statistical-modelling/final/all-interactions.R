# Read the CSV file
df <- read.csv("wine_review.csv")
df$superior_rating <- as.factor(df$superior_rating)

# Define the list of variable names
variable_names <- c("Crisp", "Dry", "Finish", "Firm", "Fresh", 
                    "Fruit", "Full", "Rich", "Round", "Soft", "Sweet", "superior_rating", "variety")

# Loop through each variable name and convert it to a factor
for (var_name in variable_names) {
  df[[var_name]] <- as.factor(df[[var_name]])
}

levels(df$superior_rating) <- c("inferior","superior")

# Function to find breakpoints for quintiles
find_breakpoints_quintiles <- function(data) {
  breaks <- quantile(data$price, probs = seq(0, 1, by = 0.2))
  return(breaks)
}

# Find breakpoints for quintiles
breaks <- find_breakpoints_quintiles(df)

# Generate labels for the factors
labels <- generate_labels(breaks)

# Create factors based on the ranges
price_factors <- cut(df$price, breaks = breaks, labels = labels, include.lowest = TRUE)

# If you want it as a column in your dataframe, you can do this:
df$price_factor <- price_factors

# Plot the mosaic plot
mosaicplot(table(df$price_factor, df$superior_rating), col=c(2,3), main = "Wine Reviews")


sample_sizes <- table(df$price_factor)

# Print sample size for each factor level
print(sample_sizes)

library("brms")

formula <- superior_rating ~ . + (.|price_factor)

stan_code <- make_stancode(formula, data=df, family=bernoulli(), prior=prior(normal(0,10),class="b"))

fit <- brm(
  formula,
  data = df,
  family = bernoulli(),
  prior = prior(normal(0, 10), class = b),
  cores = 8,
)

conditional_effects(fit)

