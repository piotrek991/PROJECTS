# Input
import numpy as np
import copy
import random
import math
import os
import time



how_many = int(input("Podaj wysokosc choinki: "));
os.system('cls')
L=[];
for x in range(how_many):
    L.append(2*x+1)
level_tree = 0;
game_field = np.array(["_"]).repeat(L[len(L)-1]+2)
game_field = np.tile(game_field,(how_many,1))
game_field_copy = np.copy(game_field);

while level_tree<how_many:
    level_to_show = len(L) - 1;
    game_field = np.copy(game_field_copy);
    level_tree_ts = level_tree;
    for y in range(level_tree+1):
        fst_star_place = int((game_field.shape[1] - L[level_to_show]) / 2)
        for x in range(fst_star_place,fst_star_place+L[level_to_show]):
            game_field[level_tree_ts,x] = "*"
        level_to_show = level_to_show - 1;
        level_tree_ts = level_tree_ts - 1;

    level_tree = level_tree+1
    print(game_field)
    print("\n\n\n")
    time.sleep(1)
    os.system('cls')



