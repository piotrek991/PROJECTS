
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


check = Solution()
data = [i for i in range(0,10000)]
data_2 = [i for i in range(10000,0,-1)]
data_f = data + data_2
data_c = [1,8,6,2,5,4,8,3,7]
#print(data_f)
print(check.maxArea(data_f))