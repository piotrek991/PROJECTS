import random
import pandas as pd

data = [random.randint(0,100) for i in range(178)]
len_d = len(data)
print(data)
for i in range(0,len_d,10):
    print(data[i:i+10])