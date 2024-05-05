source("src/df.R")
library("ggplot2")

mean_points <- aggregate(points ~ variety, data = df_all, FUN = mean)
sorted_varieties <- mean_points$variety[order(mean_points$points)]
df_all$variety <- factor(df_all$variety, levels = sorted_varieties)
df_all$value <- df_all$points / df_all$price

pdf("fig/boxplot-value.pdf")
ggplot(df_all) + geom_boxplot(aes(x = variety, 
                               y = value, 
                               fill = variety), 
                           show.legend=FALSE) + 
  labs(x = "Variety", y = "Points") + 
  theme(axis.text.x = element_text(size = 7.5)) + coord_flip()
dev.off()
