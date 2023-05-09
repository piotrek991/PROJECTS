library(ISLR)
library(ggplot2)
library(caTools)
###
stand.feature <- scale(iris[1:4])
final.data <- cbind(stand.feature,iris[5])
set.seed(101)

sample <- sample.split(final.data$Species, SplitRatio = 0.7)

train <- subset(final.data,sample == T)
test <- subset(final.data,sample == F)

library(class)

predicted.species <- knn(train[1:4],test[1:4],train$Species,k=1)
predicted.error <- mean(predicted.species != test$Species)

predicted.species <- NULL
predicted.error <- NULL
for (i in 1:10){
  predicted.species <- knn(train[1:4],test[1:4],train$Species,k=i)
  predicted.error[i] <- mean(predicted.species[i] != test$Species)
}

k.values <- 1:10
final.look <- data.frame(predicted.error,k.values)

pl <-ggplot(final.look,aes(k.values,predicted.error))+geom_point() + geom_line(lty='dotted',color='red')
plot(pl)