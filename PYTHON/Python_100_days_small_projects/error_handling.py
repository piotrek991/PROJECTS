
def make_pie(index):
    try:
        fruit = fruits[index]
    except IndexError:
        print(f"the index {index} does no exists in  fruits array")
    else:
        print(fruit + "pie")


fruits = ["A","B","c"]
total_likes = 0

make_pie(2)

facebook_posts = [
    {'Likes': 21, 'Comments': 2},
    {'Likes': 13, 'Comments': 2, 'Shares': 1},
    {'Likes': 33, 'Comments': 8, 'Shares': 3},
    {'Comments': 4, 'Shares': 2},
    {'Comments': 1, 'Shares': 1},
    {'Likes': 19, 'Comments': 3}
]
for post in facebook_posts:
    try:
        post['Likes']
    except KeyError:
        continue
    else:
        total_likes = total_likes + post["Likes"]

print(total_likes)

