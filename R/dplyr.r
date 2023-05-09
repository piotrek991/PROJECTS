library(dplyr)

df <- mtcars

#print((df, mpg > 20, cyl == 6))
#print(arrange(df,cyl,desc(wt)))
#print(select(df,mpg,hp))
#print(distinct(df,gear))
#print(mutate(df,new_col = hp/wt))
filtered.data <- filter(df,cyl == 6) %>% summarise(df,vg=mean(hp))
print(filtered.data)

