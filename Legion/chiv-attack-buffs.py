import API
from _utils import *

set_api(API)


@trap_errors
def chiv_buff_loop():
    journame = "chiv-buffs:"
    API.SysMsg(f"{journame} script started", 52)

    while not API.StopRequested:
        if not API.BuffExists(CHIV_DIVINE):
            API.SysMsg(f"{journame} cast {CHIV_DIVINE}...", 52)
            if not cast_spell(CHIV_DIVINE, None):
                break
            continue

        if not API.BuffExists(CHIV_CONSECRATE_BUFF):
            API.SysMsg(f"{journame} cast {CHIV_CONSECRATE}...", 52)
            if not cast_spell(CHIV_CONSECRATE, None):
                break
            continue

        API.SysMsg(f"{journame} buffs active, done", 52)
        return


chiv_buff_loop()
