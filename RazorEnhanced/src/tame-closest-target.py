from Scripts.src.utils import *

Journal.Clear()
while not Player.IsGhost:
    if Journal.SearchByType("You must wait a few moments to use another skill.", "System"):
        break
    if Target.HasTarget:
        Target.Cancel()
    Player.UseSkill("Animal Taming")
    Target.WaitForTarget(2000, True)
    Target.TargetExecute(Mobiles.Select(find_mobiles(range(1, 7), 2), "Nearest"))
    Misc.Pause(100)
