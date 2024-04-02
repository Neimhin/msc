df2 <- read.csv("https://www.scss.tcd.ie/~arwhite/Teaching/CS7DS3/school_compare_100.csv")
dim(df2)
df2$school <- factor(df2$school)
nlevels(df2$school)

install.packages("ggplot2")
library("ggplot2")
ggplot(df2) + geom_boxplot(aes(x = reorder(school, mathscore, median), 
                               mathscore, 
                               fill = reorder(school, mathscore, median)), 
                           show.legend=FALSE) + 
  labs(x = "School index", y = "Test score") + 
  theme(axis.text.x = element_text(size = 7.5)) + coord_flip()
ggplot(df2, aes(x = reorder(school, school, length))) + stat_count()
