class Solution(object):
    def maxSubArray(self, nums):
        global_sum = sum(nums)
        current_sum = global_sum

        local_sum = 0
        for num in nums:
            local_sum += num
            if local_sum <= num:
                local_sum = num
            if local_sum >= current_sum:
                current_sum = local_sum
        return current_sum

check = Solution()
data = [-1,-2]
print(check.maxSubArray(data))
