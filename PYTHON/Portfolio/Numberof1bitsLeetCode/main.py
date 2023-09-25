class Solution(object):
    def hammingWeight(self, n):
        mask = 0x00000001
        n = int(n,2)
        n_of_ones = int()

        for i in range(len(bin(n))):
            n_of_ones += n&mask
            n = n >> 1
        return n_of_ones

    def countBits(self, n):
        final_arr = list()
        for num in range(n+1):
            n_s = list()
            n_s.extend((bin(num)))

            n_s_arr = list(map(int,n_s[2:]))
            final_arr.append(sum(n_s_arr))
        return final_arr

check = Solution()
number = 32
print(check.countBits(number))