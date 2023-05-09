num_vec <- function(num,vec){
  count <- 0
  for (item in vec){
    if (num == item){
      count <- count + 1
    }
  }
  return(count)
}

aluminium_bar <- function(num){
  count_of_5 <- (num-num %% 5) /5
  count_of_3 <- 0
  if(num %% 5 > 0){
    count_of_3 <- num - count_of_5*5
  }
  return(count_of_5 + count_of_3)
}

sum_of_3 <- function(x,y,z){
  vec_num <- c(x,y,z)
  final_sum <- 0
  for(item in vec_num){
    if(item %% 3 != 0){
      final_sum <- final_sum + item
    }
  }
  return(final_sum)
}

is_prime <- function(num){
  count <- 0
  if(num > 1){
    for(i in 1:num){
      if(num %% i == 0)
        count <- count +1 
        if(count > 2)
          return(FALSE)
    }
  }
  else{
    return(FALSE)
  }
  return(TRUE)
  
}
result <- is_prime(61)
print(result)



