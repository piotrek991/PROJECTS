# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    guess = True
    number = random.randint(1, 1000000)
    while guess:
        print("ROUND")
        old_number = number
        number = random.randint(1, 1000000)
        print(f"The old number is : {old_number}")
        player_guess = input("Higher or lower [H/L]:")
        if player_guess.upper() == "H":
            if number > old_number:
                print(f"You guessed it right! The number was {number}")
            else:
                print("You failed! Its the end of the game")
                guess = False
        elif player_guess.upper() == "L":
            if number < old_number:
                print(f"You guessed it right! The number was {number}")
            else:
                print("You failed! Its the end of the game")
                guess = False

