# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import random

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    paper_case = ['scisors','rock']
    rock_case = ['paper', 'scisors']
    scisors_case = ['rock', 'paper']
    options = ["rock", "paper", "scisors"]
    map = [rock_case,paper_case,scisors_case]

    player_choice = int( input("Choose from the 3 options : \n1.Rock\n2.Paper\n3.Scisors\nThe number of the option you choose: "))
    computer_choice = options[random.randint(0,2)]
    while player_choice not in range(1,4):
        print("Choice is out of range please try again")
        _ = os.system('cls')
        player_choice = int(input("Choose from the 3 options : \n1.Rock\n2.Paper\n3.Scisors\nThe number of the option you choose: "))
    print(f"{options[player_choice-1]}\nvs\n{computer_choice}")
    if computer_choice == options[player_choice-1]:
        print("tie")
    elif computer_choice == map[player_choice-1][0]:
        print("you lose")
    else:
        print("You win")
