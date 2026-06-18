from Scripts.src.utils import *

currchar = chr0
healPet = get_activepet()
if is_hurt(healPet):
    mag_heal(currchar, healPet)
