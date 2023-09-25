class Solution(object):
    def __init__(self):
        self.n = int()
    def climbStairs(self, n):
        for i in range(1,3):
            if i < n:
                self.n = self.climbStairs(n-i)
            if i == n:
                return self.n + 1
        return self.n
    def ClimbStairs_opt(self,n):
        last = 1
        sec_last = 0
        for i in range(n):
            ways = last + sec_last
            sec_last = last
            last = ways
        return ways


check = Solution()
stairs = 10
print(check.climbStairs(stairs))
print(check.ClimbStairs_opt(stairs))
