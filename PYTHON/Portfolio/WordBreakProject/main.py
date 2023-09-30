class Solution(object):
    def wordBreak(self, s, wordDict):
        set_l = {len(w) for w in wordDict}
        def innerloop(s,wordDict,i):
            if i > len(s):
                return False
            elif i == len(s):
                return True
            for item in set_l:
                if s[i:i+item] in wordDict:
                    final = innerloop(s,wordDict, i+item)
                    if final:
                        return final
            return False
        return innerloop(s,wordDict,0)


check = Solution()
s = "aaaaaaa"
wordDict = ["aaa","aaaa"]
print(check.wordBreak(s,wordDict))