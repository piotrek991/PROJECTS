# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random

draw = False
player_wins = False

def check_winner(player,dealer):
    global draw
    global player_wins
    draw = False
    player_wins = False
    if (sum(player) > 21 and  sum(dealer) > 21) or sum(player) == sum(dealer):
        draw = True
    elif sum(player) > sum(dealer):
        if 21 - sum(player) >= 0:
            print(f"{sum(player)} PLAYER")
            player_wins = True
    else:
        if 21 - sum(dealer) <= 0:
            print(f"{sum(dealer)} Dealer")
            player_wins = True
    print(f"DRAW: {draw}\n PLAYER_WINS: {player_wins}")

if __name__ == '__main__':
    cards = (2,3,4,5,6,7,8,9,10,10,10,11)
    pocket = 500

    while pocket > 0:
        player_cards = [cards[random.randint(0, len(cards)-1)], cards[random.randint(0, len(cards)-1)]]
        dealer_cards = [cards[random.randint(0, len(cards)-1)],cards[random.randint(0, len(cards)-1)]]
        dealer_cards_to_show = [dealer_cards[0], "_"]

        print("SHUFFLE")
        print(f"Your current pocket: {pocket}")
        bet_sum = int(input("Input amount you bet: "))
        while True:
            print("\nROUND")
            print(f"Your cards: {player_cards}")
            print(f"dealer cards: {dealer_cards_to_show}")
            print("Do you want to HINT or STAND (choose number):")
            print("1.HINT\n2.STAND")
            if input("Place a number here: ") == "1":
                player_cards.append(cards[random.randint(0,len(cards)-1)])
            else:
                while sum(dealer_cards) < 17:
                    dealer_cards.append(cards[random.randint(0,len(cards)-1)])
                break
            if sum(player_cards) > 21:
                break
        check_winner(player_cards,dealer_cards)
        print(f"Your cards: {player_cards}")
        print(f"FINAL dealer cards: {dealer_cards}")
        if draw:
            print("Thats a draw!")
        elif player_wins:
            print("You win!")
            pocket += bet_sum
        else:
            print("You lose!")
            pocket -= bet_sum