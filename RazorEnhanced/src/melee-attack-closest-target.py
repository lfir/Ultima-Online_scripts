from Scripts.src.utils import *


def barbedwhip_specab(cts):
    # Enable the special abilities of the barbed whip and the Stagger mastery spell (if there's enough mana
    # and enemies are nearby).
    # Since Stagger has a cooldown period, only use it once every 3 times the weapon SA is used.
    if len(find_mobiles(range(3, 7), 1)) > 1:
        if (Player.Mana >= 15) and (not Player.HasSecondarySpecial):
            Player.WeaponSecondarySA()
            Misc.Pause(500)
    else:
        not_active = not (Player.SpellIsEnabled("Stagger") or Player.HasPrimarySpecial)
        if Player.Mana >= 20 and not_active:
            if cts[0] == 0 or (cts[1] - cts[0] >= 2):
                Spells.CastMastery("Stagger")
                cts[0] += 1
            else:
                Player.WeaponPrimarySA()
                cts[1] += 1
            Misc.Pause(500)


while not Player.IsGhost:
    enemies = find_mobiles(range(3, 7), 5)
    enemies_by_dist = sorted(enemies, key=lambda e: Player.DistanceTo(e))

    for enemy in enemies_by_dist:
        target = Mobiles.FindBySerial(enemy.Serial)
        attack_counters = [0, 0]

        while target and Player.InRangeMobile(target, 2):
            if Player.BuffsExist(curses[0]):
                continue
            barbedwhip_specab(attack_counters)
            Player.Attack(target)
            Misc.Pause(500)
            target = Mobiles.FindBySerial(enemy.Serial)

    Misc.Pause(500)
