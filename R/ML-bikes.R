bike <- read.csv('./CSV_files/bikeshare.csv')
#print(head(bike))
## EDA
library(ggplot2)
library(dplyr)

#CoNVERT TO POSIXCT()
bike$datetime <- as.POSIXct(bike$datetime)
plot <- ggplot(bike,aes(datetime,count)) + geom_point(alpha = 0.5,aes(color=temp))
#print(plot)
#print(plot + scale_color_continuous(low='#55D8CE',high='#FF6E2E')) + theme_bw()
bike$hour <- sapply(bike$datetime,function(x){format(x,"%H")})
bike$hour <- sapply(bike$hour,as.numeric)
#print(head(bike))

#pl <- ggplot(filter(bike,workingday==1),aes(hour,count))
#pl <- pl + geom_point(aes(color=temp))
#pl <- pl + scale_color_gradientn(colours = c('dark blue','red'))
#print(pl)

model <- lm(count ~ . - casual - registered - datetime - atemp, bike)
print(summary(model))

