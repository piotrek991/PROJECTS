import math

class Solution(object):
    def __init__(self):
        self.min = -1
        self.current =int()

    def coinChange(self, coins, amount):
        for num in coins:
            if amount - num > 0:
                self.current += 1
                self.min = self.coinChange(coins,amount-num)
                if self.current:
                    self.current -= 1
            elif amount - num == 0 or amount == 0:
                if self.min > 0:
                    self.min = min(self.current +1, self.min)
                elif amount == 0:
                    self.min = self.current
                else:
                    self.min = self.current + 1
                return self.min
        return self.min

    def coinChange_opt(self, coins: list[int], amount: int) -> int:
        def coinChangeInner(rem, cache):
            if rem < 0:
                return math.inf
            if rem == 0:
                return 0
            if rem in cache:
                return cache[rem]
            cache[rem] = min(coinChangeInner(rem - x, cache,x) + 1 for x in coins)
            return cache[rem]

        ans = coinChangeInner(amount, {})
        return -1 if ans == math.inf else ans




check = Solution()
data  = [1,2,5]
num = 11
print(check.coinChange_opt(data,num))




