def group_anagrams(words:list)->list:
    anagram_groups = list()

    while words:
        s_word = sorted(set(words[0]))
        inner_list  = list()
        words_del = words.copy()
        for item in words_del:
            if s_word == sorted(set(item)):
                inner_list.append(item)
                words.remove(item)
        anagram_groups.append(inner_list)
    return anagram_groups


def subarray_sum(nums,target):
    start_index = 0
    last_index = len(nums)
    if not nums:
        return []
    elif target in nums:
        return [nums.index(target), nums.index(target)]
    while start_index != last_index:
        if sum(nums[start_index:last_index]) != target:
            if abs(nums[start_index] - target) > abs(nums[last_index-1] - target):
                start_index += 1
            else:
                last_index -= 1
        else:
            return [start_index, last_index - 1]
    return []


nums = [3, 6, 0, 1, 1]
target = 9
print ( subarray_sum(nums, target) )