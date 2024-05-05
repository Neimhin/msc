library("ggplot2")
library("ggmosaic")
df <- read.csv("wine_review.csv")
mosaicplot(table(df$variety, df$superior_rating), col=c(2,3), main = "Wine Reviews")
library(ggplot2)
library(ggmosaic)

# Read the data
df <- read.csv("wine_review.csv")

# Get unique variety names
varieties <- unique(df$variety)

# Create variety names using seq_along
variety_names <- paste0("var", seq_along(varieties))

# Create a mapping table
mapping_table <- data.frame(variety = varieties, variety_name = variety_names)

# Merge mapping table to rename varieties
df <- merge(df, mapping_table, by = "variety")

# Plot mosaic plot
t <- table(df$variety)
print(sort(t))
mosaicplot(t, col=c(2,3), main = "Wine Reviews")
