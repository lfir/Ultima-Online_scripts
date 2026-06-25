import API
from _utils import *

set_api(API)


@trap_errors
def chiv_heal_loop():
    API.SysMsg("**Chiv self-heal** script started.", 52)

    while not API.StopRequested:
        poisoned = API.Player.IsPoisoned
        damaged = API.Player.Hits < API.Player.HitsMax
        cursed = is_cursed()
        ps = API.Player.Serial

        if not poisoned and not damaged and not cursed:
            API.SysMsg("No conditions to treat. Done.", 52)
            return

        if poisoned:
            API.SysMsg(f"Casting {CHIV_CLEANSE}...", 52)
            if not cast_spell(CHIV_CLEANSE, ps):
                return
            continue

        if damaged:
            API.SysMsg(f"Casting {CHIV_CLOSE_WOUNDS}...", 52)
            if not cast_spell(CHIV_CLOSE_WOUNDS, ps):
                return
            continue

        if cursed:
            API.SysMsg(f"Casting {CHIV_RM_CURSE}...", 52)
            if not cast_spell(CHIV_RM_CURSE, ps):
                return
            continue


chiv_heal_loop()
