import API
import _utils
from _utils import cast_spell, is_cursed

_utils.init(API)


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
