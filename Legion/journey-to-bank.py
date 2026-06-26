import API
from _utils import cast_spell, set_api, trap_errors, CHIV_JOURNEY

set_api(API)

RUNEBOOK_SERIAL = 1081895304


@trap_errors
def journey_to_bank():
    journame = "journey-to-bank:"
    API.SysMsg(f"{journame} script started", 52)

    API.SysMsg(f"{journame} cast {CHIV_JOURNEY}...", 52)
    cast_spell(CHIV_JOURNEY, RUNEBOOK_SERIAL)


journey_to_bank()
