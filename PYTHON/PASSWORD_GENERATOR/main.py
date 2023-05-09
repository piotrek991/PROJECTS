# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import string
import random

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    alphabet = string.ascii_letters
    numbers = list(range(0,10))
    symbols = list(string.printable[-7:-(len(string.printable)-(len(alphabet)+len(numbers))):-1])
    length = int(input("How long your password should be?: "))
    amount_symbols = int(input("How many symbols? :"))
    amount_numbers = int(input("How many numbers? :"))
    amount_letters = length-amount_numbers-amount_numbers
    map = [alphabet,symbols,numbers]
    random_choice = 0
    final_password = ""
    while amount_numbers > 0 or amount_symbols > 0 or amount_letters > 0:
        type_of_character = random.randint(1,3)
        if type_of_character == 2 and amount_symbols > 0:
            random_choice = random.randint(0,len(symbols)-1)
            final_password = final_password + symbols[random_choice]
            amount_symbols -= 1
        elif type_of_character == 3 and amount_numbers > 0:
            random_choice = random.randint(0,len(numbers)-1)
            final_password = final_password + str(numbers[random_choice])
            amount_numbers -= 1
        elif type_of_character == 1 and amount_letters > 0:
            random_choice = random.randint(0,len(alphabet)-1)
            final_password = final_password + alphabet[random_choice]
            amount_letters -= 1
    print(final_password)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
