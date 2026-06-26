import API
from _utils import *

set_api(API)


@trap_errors
def chiv_heal_loop():
    journame = "self-heal:"
    API.SysMsg(f"{journame} script started", 52)

    while not API.StopRequested:
        poisoned = API.Player.IsPoisoned
        damaged = API.Player.Hits < API.Player.HitsMax
        cursed = is_cursed()
        ps = API.Player.Serial

        if poisoned:
            API.SysMsg(f"{journame} cast {CHIV_CLEANSE}...", 52)
            if not cast_spell(CHIV_CLEANSE, ps):
                break
            continue

        if damaged:
            API.SysMsg(f"{journame} cast {CHIV_CLOSE_WOUNDS}...", 52)
            if not cast_spell(CHIV_CLOSE_WOUNDS, ps):
                break
            continue

        if cursed:
            API.SysMsg(f"{journame} cast {CHIV_RM_CURSE}...", 52)
            if not cast_spell(CHIV_RM_CURSE, ps):
                break
            continue

        API.SysMsg(f"{journame} no conditions to treat, done", 52)
        return


chiv_heal_loop()
