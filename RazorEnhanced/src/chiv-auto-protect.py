from Scripts.src.utils import *

currchar = chr1
grave_curses = curses[:8]

while not Player.IsGhost:
    if (Player.Hits <= (Player.HitsMax - 60)) or (Player.Poisoned and not Player.BuffsExist("Vampiric Embrace")):
        chiv_heal(currchar, playermob)
    if Player.BuffsExist(curses[0]):
        Player.HeadMessage(40, "BlOOD OATH!!! RUN!!!")
        Player.SetWarMode(False)
    if Player.Poisoned:
        continue
    if any(map(Player.BuffsExist, grave_curses)):
        cast("Remove Curse", currchar, playermob)
    if not Player.BuffsExist("Consecrate Weapon"):
        cast("Consecrate Weapon", currchar)
    if currchar.get("usesdf") and (not Player.BuffsExist("Divine Fury")):
        cast("Divine Fury", currchar)
    Misc.Pause(500)
