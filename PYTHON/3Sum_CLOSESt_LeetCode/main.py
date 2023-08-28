import math

class Solution(object):
    def find_closest(self,num,array):
            
    def threeSumClosest(self, nums, target):
        positive_part = [i for i in nums if i >= 0]
        negative_part = [i for i in nums if i < 0]

        postive_orig = positive_part[:]
        negative_orig = negative_part[:]

        final_nums = 0
        if min(positive_part) < abs(max(negative_part)):
            final_nums = min(positive_part)
            positive_part.pop(positive_part.index(min(positive_part)))
        else:
            final_nums = max(negative_part)
            negative_part.pop(negative_part.index(max(negative_part)))

        for i in range(2)


        if target >= 0:

