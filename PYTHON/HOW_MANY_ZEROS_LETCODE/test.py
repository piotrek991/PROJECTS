def count_sum(num):
    if num == 0 : return 0
    return num + count_sum(num-1)

print(count_sum(3))