class Solution(object):
    def twoSum(self, nums, target):
        for location,item in enumerate(nums):
            check_array = nums[:]
            check_array[location] = None
            if (target - item) in check_array:
                return [location, check_array.index(target-item)]
        return list()


object_check = Solution()
num = [3,2,4]
targets = 6
