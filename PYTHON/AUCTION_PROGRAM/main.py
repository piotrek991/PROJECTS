# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def find_max(dict):
    max = dict[next(iter(dict))]
    for key in dict:
        if dict[key] > max:
            max = dict[key]
    return max

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    bids = {}
    while True:
        name = input("Podaj imie pierwszego bidera: ")
        bid_value = int(input("Podaj wartosc bida: "))
        bids[name] = bid_value
        if 'N' in input("Chcialbys wprowadzic kolejnego uczestnika ? [T/N]"):
            break
    print(f"The winner name is {[key for key in bids if bids[key] == find_max(bids)][0]} with the bid {find_max(bids)}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
