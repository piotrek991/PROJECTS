import random
class Solution(object):
    def __init__(self):
        self.sol = list()
    #works but memory exceeded error when list is too big
    def maxProfit(self, prices):
        global_min, global_max = min(prices),max(prices)
        if prices.index(global_max) > prices.index(global_min):
            self.sol.append(global_max-global_min)
            return self.sol[0]
        prices_copy = prices.copy()
        prices_copy.sort(reverse=True)
        if prices == prices_copy:
            return 0
        not_match = False
        while not not_match:
            if prices_copy[-1] == prices[-1]:
                prices.pop(-1)
                prices_copy.pop(-1)
            else:
                not_match = True
        left = prices[:prices.index(global_max)+1]
        right = prices[prices.index(global_max)+1:]

        if len(left) > 1:
            self.maxProfit(left)
        if len(right) > 1:
            self.maxProfit(right)
        if self.sol:
            return max(self.sol)
        return 0

check = Solution()
data = [i if i > 10000 else 0 for i in range(40000,0,-1)]
data_test = [2,1,2,1,0,1,2]

print(check.maxProfit(data_test))



