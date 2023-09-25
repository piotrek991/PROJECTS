
class Solution(object):
    def maxArea(self, height):
        len_h = len(height)

        max_i = int()
        max_v = int()

        for i in range(len_h):
            if height[i] > max_i:
                max_i = height[i]
                length_to_beat = max_v // height[i]
                data_p = {location+length_to_beat+i+1:item for location, item in enumerate(height[length_to_beat+i+1:]) if item >= height[i]}
                if data_p:
                    current_l = list(data_p)[-1]
                    current_last_i = data_p[current_l]
                    max_v = max(min(height[i], current_last_i) * (current_l - i), max_v)
                else:
                    current_l = length_to_beat + i

                for j in range(current_l+1, len_h):
                    max_v = max(height[j]*(j-i),max_v)

        return max_v




    def maxArea_opt(self, height):
        len_h = len(height)
        current_m = int()
        for i in range(len_h):
            for j in range(i+1,len_h):
                space_m = min(height[i],height[j]) * (j-i)
                current_m = max(current_m,space_m)
        return current_m

    def getSum(self, a: int, b: int) -> int:

        # 32 bit mask in hexadecimal
        mask = 0xffffffff

        # works both as while loop and single value check
        while (b & mask) > 0:
            carry = (a & b) << 1

            a = (a ^ b)
            b = carry
            print(bin(a,b)

        # handles overflow
        return (a & mask) if b > 0 else a

check = Solution()
#print(data_f)
print(check.getSum(2,3))