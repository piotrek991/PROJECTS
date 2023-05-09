library(Amelia)
library(dplyr)
library(caTools)

adult <- read.csv('./CSV_files/adult_sal.csv')
adult <- select(adult,-X)
#####
unemp <- function(job){
  job <- as.character(job)
  if(job == 'Never-worked' | job == 'Without-pay'){
    return('Unemployed')
  }else{
    return(job)
  }
}
adult$type_employer <- sapply(adult$type_employer,unemp)
group_emp <- function(job){
  job <- as.character(job)
  if(job == 'Local-gov' | job == 'State-gov'){
    return('SL-gov')
  }
  else if(job == 'Self-emp-inc' | job == 'Self-emp-not-inc'){
    return('self-emp')
  }
  else{
    return(job)
  }
}
adult$type_employer <- sapply(adult$type_employer,group_emp)
group_martial <- function(mar){
  mar <- as.character(mar)
  if(mar == 'Separated' | mar == 'Divorced' | mar == 'Widowed'){
    return('Not-Married')
  }
  else if(mar == 'Never-married'){
    return(mar)
  }
  else{
    return('Married')
  }
}
adult$marital <- sapply(adult$marital,group_martial)

Asia <- c('China','Hong','India','Iran','Cambodia','Japan', 'Laos' ,
          'Philippines' ,'Vietnam' ,'Taiwan', 'Thailand')

North.America <- c('Canada','United-States','Puerto-Rico' )

Europe <- c('England' ,'France', 'Germany' ,'Greece','Holand-Netherlands','Hungary',
            'Ireland','Italy','Poland','Portugal','Scotland','Yugoslavia')

Latin.and.South.America <- c('Columbia','Cuba','Dominican-Republic','Ecuador',
                             'El-Salvador','Guatemala','Haiti','Honduras',
                             'Mexico','Nicaragua','Outlying-US(Guam-USVI-etc)','Peru',
                             'Jamaica','Trinadad&Tobago')
Other <- c('South')

group_country <- function(ctry){
  if (ctry %in% Asia){
    return('Asia')
  }else if (ctry %in% North.America){
    return('North.America')
  }else if (ctry %in% Europe){
    return('Europe')
  }else if (ctry %in% Latin.and.South.America){
    return('Latin.and.South.America')
  }else{
    return('Other')      
  }
}
adult$country <- sapply(adult$country,group_country)

adult[adult == '?'] <- NA
adult$type_employer <- sapply(adult$type_employer,factor)
adult$country <- sapply(adult$country,factor)
adult$marital <- sapply(adult$marital,factor)
adult$education <- sapply(adult$education,factor)
adult$occupation <- sapply(adult$occupation,factor)
adult$relationship  <- sapply(adult$relationship ,factor)
adult$race <- sapply(adult$race,factor)
adult$sex <- sapply(adult$sex,factor)
adult$income <- sapply(adult$income,factor)

adult <- na.omit(adult)
adult <- rename(adult,region = country)


##MODEL LOGISTIC##
set.seed(101)
sample <- sample.split(adult$income,SplitRatio = 0.7)

train <- subset(adult,sample == T)
test <- subset(adult,sample == F)

