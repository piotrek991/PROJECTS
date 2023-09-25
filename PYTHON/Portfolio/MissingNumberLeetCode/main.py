class Solution(object):
    def missingNumber(self, nums):
        data_prop = [i for i in range(len(nums)+1)]
        print(data_prop)
        return sum(data_prop) - sum(nums)

    def reverseBits(self, n):
        data_n = bin(n)
        initial_l = 34 - len(data_n)
        s_rev = data_n[2:][::-1]
        if initial_l:
            return int(s_rev,2) << initial_l
        return int(s_rev,2)


check = Solution()
nums = 0b00000010100101000001111010011100
print(check.reverseBits(nums))