df <- read.csv("wine_review.csv")


print(table(df$superior_rating, df$Rich))

# Read the CSV file
df <- read.csv("wine_review.csv")

# Define the names for rows and columns
row_names <- c("Inferior", "Superior")
col_names <- c("Not Rich", "Rich")

# Create the contingency table with proper names
contingency_table <- table(df$superior_rating, df$Rich, dnn = list("Superior Rating" = row_names, "Rich" = col_names))

# Print the contingency table
print(contingency_table)

