df <- read.csv("wine_review.csv")
set.seed(42)
df <- df[sample(1:nrow(df)),]
df$log_price = log(df$price)
# df$points.c <- df$points - 90
# df$log2_price = log(df$price, base=2)
# df$log2_price.c <- df$log2_price - 5
df$rich_and_full <- df$Rich & df$Full
df$soft_and_crisp <- df$Soft & df$Crisp
df_test <- df[2000:2500,]
df_all <- df[1:2500,]
df <- df[1:2000,]
