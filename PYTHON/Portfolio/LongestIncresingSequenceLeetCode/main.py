class Solution(object):
    def lengthOfLIS_opt(self, nums):
        longest_streak = 1
        actual_streak = 1
        last_min = nums[0]

        last_num_h = [nums[0]]
        last_num_list = [nums[0]]
        for i in range(1,len(nums)):
            if nums[i] < last_min:
                last_min = nums[i]
                actual_streak = 1
                last_num_h = [nums[i]]
            elif nums[i] < last_num_h[-1] and nums[i] > last_min:
                bigger_i_l = len([item for item in last_num_h if item < nums[i]])
                actual_streak -= (len(last_num_h) - bigger_i_l)
                last_num_h = last_num_h[:bigger_i_l]

            if nums[i] > last_min and nums[i] > last_num_h[-1]:
                if nums[i] > last_num_list[-1]:
                    last_num_list.append(nums[i])
                actual_streak += 1
                last_num_h.append(nums[i])
            if actual_streak > len(last_num_list):
                longest_streak = actual_streak
                last_num_list = last_num_h.copy()
        return max(longest_streak,len(last_num_list))

    def lengthOfLIS_opt2(self, nums):
        list_greater = list()
        actual_length = 0
        for i in range(1,len(nums)):
            list_greater.append(sum(nums[i] > number for number in nums[:i]))

        for j in range(1,len(list_greater)):
            print(list_greater[j],actual_length)
            if list_greater[j] > 0:
                if list_greater[j] > list_greater[j-1]:
                    actual_length = list_greater[j] - actual_length
                else:
                    actual_length = list_greater[j] + 1
            else:
                actual_length = 1
        print(list_greater)
        return actual_length

    def lengthOfLIS(self, nums):
        tails = [0] * len(nums)
        size = 0
        for x in nums:
            i, j = 0, size
            while i != j:
                m = (i + j) // 2
                if tails[m] < x:
                    i = m + 1
                else:
                    j = m
            tails[i] = x
            size = max(i + 1, size)
            print(tails, size)
        return size

check = Solution()
nums = [11,12,13,0,5,-1,6,7,8]
print(check.lengthOfLIS(nums))