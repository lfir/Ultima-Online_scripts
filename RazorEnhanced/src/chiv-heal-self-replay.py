from Scripts.src.utils import *

currchar = chr1

while is_hurt(Player):
    chiv_heal(currchar, playermob)
if player_cursed():
    cast("Remove Curse", currchar, playermob)
