

class Solution(object):
    def threeSum_optv2(self, nums):
        positive = [number for number in nums if number >= 0]
        negative = [number for number in nums if number < 0]
        zeros = [number for number in nums if number == 0]

        final_array = list()
        list_sets = list()

        for num in nums:
            if num > 0:
                positive.remove(num)
                for item in negative:
                    if 0 - item - num in positive:
                        if not {num, item, 0 - item - num} in list_sets:
                            final_array.append([num, item, 0 - item - num])
                            list_sets.append({num, item, 0 - item - num})
                positive.append(num)
            elif num < 0:
                negative.remove(num)
                for item in positive:
                    if 0 - item - num in negative:
                        if not {num, item, 0 - item - num} in list_sets:
                            final_array.append([num, item, 0 - item - num])
                            list_sets.append({num, item, 0 - item - num})
                negative.append(num)
            else:
                zeros.remove(0)
                if len(zeros) >=2:
                    if not {0,0,0} in list_sets:
                        final_array.append([0,0,0])
                        list_sets.append({0,0,0})
                        zeros.remove(0)
                        zeros.remove(0)

        return final_array


    def threeSum_opt(self, nums):
        final_array =list()
        list_of_sets = list()
        local_array = list()

        for num in nums[:-1]:
            local_array = nums.copy()
            local_array.remove(num)
            for number in nums[nums.index(num)+1:]:
                local_array.remove(number)
                if 0 - num - number in local_array:
                    if not {num,number,0 - num - number} in list_of_sets:
                        final_array.append([num,number,0 - num - number])
                        list_of_sets.append({num,number,0 - num - number})
                    continue
                local_array.append(number)

        return final_array

check = Solution()
data = [-1,0,1,0]
print(check.threeSum(data))
