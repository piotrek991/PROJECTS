from functools import lru_cache
class Solution(object):
    def wordBreak(self, s, wordDict):
        set_l = {len(w) for w in wordDict}

        @lru_cache(maxsize=1000)
        def innerloop(i):
            if i > len(s):
                return False
            elif i == len(s):
                return True
            for item in set_l:
                if s[i:i+item] in wordDict:
                    final = innerloop(i+item)
                    if final:
                        return final
            return False
        return innerloop(0)


check = Solution()
s = "leetcode"
wordDict = ["leet","code"]
print(check.wordBreak(s,wordDict))