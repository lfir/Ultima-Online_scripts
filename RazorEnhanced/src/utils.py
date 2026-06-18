from AutoComplete import *

# Variables related to different characters
chr0 = {"fcrdelay": 0}  # 6 FCR
chr1 = {"fcrdelay": 1600, "usesdf": False}  # 2 FCR
playermob = Mobiles.FindBySerial(Player.Serial)
# Spell mana costs
spells = {
    # Fourth Circle
    "Arch Cure": 11,
    "Greater Heal": 11,
    "Recall": 11,
    # Sixth Circle
    "Invisibility": 20,
    # Chivalry
    "Close Wounds": 10,
    "Cleanse by Fire": 10,
    "Consecrate Weapon": 10,
    "Divine Fury": 10,
    "Remove Curse": 20,
    "Sacred Journey": 20
}
curses = ["Bload Oath (curse)", "Corpse Skin", "Curse", "Evil Omen", "Mind Rot",
          "Mortal Strike", "Paralyze", "Clumsy", "Feeble Mind", "Strangle", "Weaken"]
# Pet serial numbers
shadow_wyrm = 0x1DB18
naja = 0x0002FF2C
toothless = 0x0003A06D
pets = [shadow_wyrm, naja, toothless]


def cast(spell, caster, target=None):
    if Player.Mana >= spells.get(spell):
        if target and Target.HasTarget():
            Target.Cancel()
        Spells.Cast(spell)
        if target:
            Target.WaitForTarget(2000, True)
            Target.TargetExecute(target)
        Misc.Pause(caster.get("fcrdelay"))


def chiv_heal(caster, target):
    if target.Poisoned:
        cast("Cleanse by Fire", caster, target)
    else:
        cast("Close Wounds", caster, target)


def mag_heal(caster, target):
    if target.Poisoned:
        cast("Arch Cure", caster, target)
    else:
        cast("Greater Heal", caster, target)


def player_cursed():
    return any(map(Player.BuffsExist, curses))


def is_hurt(target, hpdiff=0):
    return (target.Hits < (target.HitsMax - hpdiff)) or target.Poisoned


def find_mobiles(notorieties, maxrange):
    # 1: blue; 2: green; 3: gray, neutral
    # 4: gray, criminal; 5: orange; 6: red
    mobilefilter = Mobiles.Filter()
    mobilefilter.RangeMax = maxrange
    for n in notorieties:
        mobilefilter.Notorieties.Add(n)
    mobilefilter.CheckIgnoreObject = True
    mobilefilter.CheckLineOfSight = True
    return Mobiles.ApplyFilter(mobilefilter)


def get_activepet():
    # Only one should be active at a time
    return next(filter(lambda p: p, map(Mobiles.FindBySerial, pets)))
