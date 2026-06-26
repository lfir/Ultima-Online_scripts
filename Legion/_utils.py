import functools
import math

_api = None


def set_api(api):
    global _api  # required: without this, assignment would create a local variable
    if _api is None:
        _api = api


def trap_errors(func):
    """Decorator: catches unhandled exceptions and reports them via SysMsg."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            _api.SysMsg(f"{func.__name__} error: {e}", 33)

    return wrapper


CHIV_CLEANSE = "Cleanse by Fire"
CHIV_CLOSE_WOUNDS = "Close Wounds"
CHIV_RM_CURSE = "Remove Curse"
CHIV_JOURNEY = "Sacred Journey"

# Mana costs for each spell (base, before Lower Mana Cost).
SPELL_MANA_COSTS = {
    CHIV_CLEANSE: 10,
    CHIV_CLOSE_WOUNDS: 10,
    CHIV_RM_CURSE: 20,
    CHIV_JOURNEY: 20,
}

# Spells that require a "Neutral" target cursor.
_NEUTRAL_SPELLS = {CHIV_JOURNEY}

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


def _cursor_type_for(spell_name):
    return "Neutral" if spell_name in _NEUTRAL_SPELLS else "Beneficial"


def cast_spell(spell_name, target):
    """Check mana, cast spell, acquire target (or skip if None), then wait for cr_delay (character-scoped variable)
    or 2 seconds by default if undefined (recovery time for a char with 0 FCR).

    Returns True if the spell was cast, False if mana was insufficient.
    """
    lmc = _api.Player.LowerManaCost / 100.0
    cost = math.ceil(SPELL_MANA_COSTS[spell_name] * (1.0 - lmc))
    if _api.Player.Mana < cost:
        _api.SysMsg(
            f"Not enough mana for {spell_name} (need {cost}, have {_api.Player.Mana}).",
            33,
        )
        return False

    _api.CastSpell(spell_name)
    if target is not None and _api.WaitForTarget(_cursor_type_for(spell_name), 3):
        _api.Target(target)
    _api.Pause(int(_api.GetPersistentVar("cr_delay", "2", _api.PersistentVar.Char)))

    return True


def is_cursed():
    """Return True if the player has any debuff that Remove Curse can remove."""
    return any(_api.BuffExists(curse) for curse in REMOVABLE_CURSES)


def get_mobs_by(notorieties, dist):
    """Return all mobiles within *dist* tiles matching any of *notorieties*.

    Queries each notoriety separately because NearestMobiles returns None when
    multiple notorieties are passed in one call.
    """
    mobs = []
    for n in notorieties:
        inrange = _api.NearestMobiles([n], dist)
        if inrange:
            mobs.extend(inrange)

    return mobs
