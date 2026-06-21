import math
import API

# Mana costs for each spell (base, before Lower Mana Cost).
SPELL_MANA_COSTS = {
    "Cleanse by Fire": 10,
    "Close Wounds": 10,
    "Remove Curse": 20,
}

# All debuffs the chivalry Remove Curse spell can remove.
REMOVABLE_CURSES = [
    "Curse",
    "Clumsy",
    "Weaken",
    "Feeblemind",
    "Paralyze",
    "Corpse Skin",
    "Evil Omen",
    "Mind Rot",
    "Strangle",
    "Blood Oath",
    "Mortal Strike",
]


def cast_spell(spell_name, target):
    """Check mana, cast spell, acquire target (or skip if None), then wait 1.5 s.

    Returns True if the spell was cast, False if mana was insufficient.
    """
    lmc = API.Player.LowerManaCost / 100.0
    cost = math.ceil(SPELL_MANA_COSTS[spell_name] * (1.0 - lmc))
    if API.Player.Mana < cost:
        API.SysMsg(
            f"Not enough mana for {spell_name} (need {cost}, have {API.Player.Mana}).",
            33,
        )
        return False

    API.CastSpell(spell_name)
    if target is not None and API.WaitForTarget("Beneficial", 3):
        API.Target(target)
    API.Pause(2)

    return True


def is_cursed():
    return any(API.BuffExists(curse) for curse in REMOVABLE_CURSES)


def chiv_heal_loop():
    API.SysMsg("Chiv self-heal started.")

    try:
        while not API.StopRequested:
            poisoned = API.Player.IsPoisoned
            damaged = API.Player.Hits < API.Player.HitsMax
            cursed = is_cursed()

            if not poisoned and not damaged and not cursed:
                API.SysMsg("No conditions to treat. Done.")
                return

            if poisoned:
                API.SysMsg("Casting Cleanse by Fire...")
                if not cast_spell("Cleanse by Fire", API.Player.Serial):
                    return
                continue

            if damaged:
                API.SysMsg("Casting Close Wounds...")
                if not cast_spell("Close Wounds", API.Player.Serial):
                    return
                continue

            if cursed:
                API.SysMsg("Casting Remove Curse...")
                if not cast_spell("Remove Curse", API.Player.Serial):
                    return
                continue

    except Exception as e:
        API.SysMsg(f"Chiv self-heal error: {e}", 33)


chiv_heal_loop()
