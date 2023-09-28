import math
class Solution(object):
    def longestCommonSubsequence(self, text1, text2):
        if len(text1) < len(text2):
            longer = text2
            shorter = text1
        else:
            longer = text1
            shorter = text2

        arr = [math.inf] * len(longer)
        arr_l = [""] * len(longer)
        size = 0
        size_a = 0
        print(longer,shorter)
        for z in range(len(longer)):
             i,j = 0, size_a
             if longer[z] in shorter:
                count_l = arr_l.count(longer[z])
                l_ind = -1
                if count_l:
                    for i in range(count_l):
                        l_ind = shorter.index(longer[z],l_ind+1)
                ind = shorter.find(longer[z],l_ind + 1)
                if ind > -1:
                    while i != j:
                        m = (i+j) // 2
                        if ind > arr[m]:
                            i = m + 1
                        else:
                            j = m
                    size_a = i+1
                    arr[i:] = [math.inf] * (len(arr) - i)
                    arr[i] = ind
                    arr_l.append(shorter[ind])
                size = max(i+1,size)
        return size


check = Solution()
text1 = "abcde"
text2 = "ace"

print(check.longestCommonSubsequence(text1,text2))


