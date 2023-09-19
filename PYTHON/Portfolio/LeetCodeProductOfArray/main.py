import functools
class Solution(object):
    def productExceptSelf(self, nums):
        data_diff_zero = [num for num in nums if num]
        try:
            data_mult = functools.reduce(lambda x,y: x*y,data_diff_zero)
        except Exception as e:
            data_mult = 0
        diff = len(nums) - len(data_diff_zero)
        if diff == 1:
            return [data_mult if not num else 0 for num in nums]
        if diff > 1:
            return [0]*len(nums)
        final_result = list()
        for num in nums:
            final_result.append(data_mult//num)
        return final_result

check = Solution()
nums = [0,4,0]
print(check.productExceptSelf(nums))
