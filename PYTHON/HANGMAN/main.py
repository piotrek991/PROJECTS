# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
def is_blank(word):
    for i in range(len(word)):
        if word[i] == "_":
            return True
    return False
def check_letter(letter,word):
    positions = []
    for i in range(len(word)):
        if letter == word[i]:
            positions.append(i)
    return positions
def already_guessed(tab, letter):
    for x in tab:
        if x == letter:
            return True
    return False
if __name__ == '__main__':
    words = ['ardvark','baboon','camel']
    guesses =[]
    choosen = words[random.randint(0,len(words)-1)]
    guess = ""
    lives = 7
    for i in range(len(choosen)):
        guess = guess + "_"
    while is_blank(guess):
        print(f"{guess}")
        letter = input("Podaj litere :")
        while already_guessed(guesses,letter):
            print("Wczesnie sprawdza, sproboj cos innego")
            letter = input("Podaj litere :")
        guesses.append(letter)
        letter.lower()
        positions = check_letter(letter,choosen)
        if positions:
            print("Trafione")
            for i in range(len(positions)):
                guess = guess[:positions[i]] + choosen[positions[i]] + guess[positions[i]+1:]
        else:
            lives -= 1
            if (lives == 0):
                print("\nPrzegrales")
                exit()
            print(f"Brak litery, pozostalo {lives} prob")
    print(f"WYGRALES\nTWOJE SLOWO TO: {guess}")






