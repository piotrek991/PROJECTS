import numpy as np
import random
from os import system
from time import sleep

def generate_game_field():
    z = np.arange(1,11)
    y = [" "];
    for i in range(10):
        letter = chr(65+i)
        y.append(letter);

    x = np.array(["_"]).repeat(10);
    x = np.tile(x, (10, 1));
    y = np.reshape(y,(11,1))

    z = np.vstack([z, x])
    z = np.hstack([y,z])
    return z
def show_game_field(x):
    print(x)
def generate_ships(ships_field):
    sum_of_ships = 0;
    for x in how_many:
        sum_of_ships = how_many[x];
        while(sum_of_ships):
            y_position = random.randint(0,9)
            x_position = random.randint(0,9)
            rand_direction = random.randint(0,1);
            while(will_not_crash(x_position,y_position,x,rand_direction,ships_field) != True):
                #print(will_not_crash(x_position,y_position,x,rand_direction));
                #print(willfit(x_position,y_position,rand_direction,x));
                y_position = random.randint(0, 9)
                x_position = random.randint(0, 9)
                rand_direction = random.randint(0, 1);
                #print(y_position, " ", x_position, " ", rand_direction, " ",x);

            for y in range(x):
                ships_field[x_position][y_position] = "X";
                if (rand_direction == 1):
                    x_position += 1;
                elif (rand_direction == 0):
                    y_position += 1;
            sum_of_ships -=1;


def willfit(x_position,y_position,direction,size):
    #direction 1 - x, 0 -y
    if(direction == 1):
        if(x_position+size > 10):
            return False
        else:
            return True
    elif(direction == 0):
        if (y_position + size > 10):
            return False
        else:
            return True
def will_not_crash(x_position, y_position, size,direction,ships_field):
    # direction 1 - x, 0 -y
    if(willfit(x_position,y_position,direction,size)):
        c_ships_field = np.copy(ships_field)
        for x in range(size):
            if(ships_field[x_position][y_position] != '_'):
                return False
            if(direction == 1):
                x_position+=1;
            elif(direction ==  0):
                y_position+=1;
        return True
    else:
        return False



def generate_ships_map():
    field = np.array(["_"]).repeat(10);
    field = np.tile(field,(10,1));
    return field;
def sum_of_ships(ships_field):
    sum = 0;
    for x in range(10):
        for y in range(10):
            if(ships_field[x][y] == "X"):
                sum += 1;
    return sum

def check_opponent_side(ships_field, x_position, y_position):
     if(ships_field[x_position, y_position] == "X"):
         return True
     else:
         return False

def game_signs():
    print("*****WITAJ W GRZE W STATKI*****")
    print("POLA ZOSTALY WYGENEROWANE AUTOMATYCZNIE")
    print("MAPA GRACZA NR 1 : ")
    print(map_field_1, "\n")
    print("MAPA GRACZA NR 2 : ")
    print(map_field_2, "\n")



how_many = {6:1,4:2,3:2,2: 2}  # how many ships of each size
map_field_1 = generate_game_field();
map_field_2 = generate_game_field();
ships_field_1 = generate_ships_map();
ships_field_2 = generate_ships_map();
generate_ships(ships_field_1);
generate_ships(ships_field_2);
# print(map_field_1)
# print(map_field_2)
# print(ships_field_2)

turn = random.randint(1,2);

system("cls")
name_1 = input("Podaj Imie gracza nr 1: ")
name_2 = input("Podaj Imie gracza nr 2: ")

while ((sum_of_ships(ships_field_1) > 0) and (sum_of_ships(ships_field_2) > 0)):
    game_signs()
    if(turn == 1):
        print("Kolejka gracza o imieniu: ", name_1)
        guess = input("Podaj numer pola na obszarze przeciwnika : ")
        x_position = ord(guess[0]) - 65;
        if (len(guess) > 2):
            y_position = int(guess[1:3]) - 1;
        else:
            y_position = int(guess[1]) - 1;

        while(check_opponent_side(ships_field_2, x_position, y_position)):
            print("TRAFIONY!")
            sleep(1);
            map_field_2[x_position+1][y_position+1] = "Y";
            ships_field_2[x_position][y_position] = "_"
            system("cls")

            game_signs()
            print("Kolejka gracza o imieniu: ", name_1)
            guess = input("Podaj numer pola na obszarze przeciwnika : ")
            x_position = ord(guess[0]) - 65;
            if (len(guess) > 2):
                y_position = int(guess[1:3]) - 1;
            else:
                y_position = int(guess[1]) - 1;
        print("PRZESTRZELILES");
        sleep(1);
        system("cls")
        turn = 2;
    else:
        print("Kolejka gracza o imieniu: ", name_2)
        guess = input("Podaj numer pola na obszarze przeciwnika : ")
        x_position = ord(guess[0]) - 65;
        if (len(guess) > 2):
            y_position = int(guess[1:3]) - 1;
        else:
            y_position = int(guess[1]) - 1;

        while(check_opponent_side(ships_field_2, x_position, y_position)):
            print("TRAFIONY!")
            sleep(1);
            map_field_1[x_position+1][y_position+1] = "Y";
            ships_field_1[x_position][y_position] = "_"
            system("cls")

            game_signs()
            print("Kolejka gracza o imieniu: ", name_2)
            guess = input("Podaj numer pola na obszarze przeciwnika : ")
            x_position = ord(guess[0]) - 65;
            if (len(guess) > 2):
                y_position = int(guess[1:3]) - 1;
            else:
                y_position = int(guess[1]) - 1;
        print("PRZESTRZELILES");
        system("cls")
        turn = 1;
        sleep(1);

