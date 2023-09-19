class Solution(object):
    def containsDuplicate(self, nums):
        copy = set()
        for location,number in enumerate(nums):
            copy.add(number)
            if location > 0:
                if number in copy:
                    return True
        return False

check = Solution()

data = [i for i in range(10**5)]
print(check.containsDuplicate(data))