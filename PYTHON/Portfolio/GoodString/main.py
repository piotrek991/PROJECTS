import random
s = "aaaabbbbcccdddeeffg"

string_good = False
count = 0
while not string_good:
    action = False
    s_counts = {letter: s.count(letter) for letter in s}
    s_nested = {count: list(s_counts.values()).count(count) for count in s_counts.values()}
    if any(c > 1 for c in s_nested.values()):
        max_count_count = max(list(s_nested.values()))
        count_index = list(s_nested.keys())[list(s_nested.values()).index(max_count_count)]

        letters_max = [letter for letter,count in s_counts.items() if count == count_index]
        string_list = [*s]
        string_list[string_list.index(letters_max[0])] = ""
        s = "".join(string_list)
        print(s)
        action = True
        count += 1
    if not action:
        string_good = True

print(f"Indicies to be delted to obtain good string: {count}")



