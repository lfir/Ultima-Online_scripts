import API
from _utils import get_mobs_by, set_api, trap_errors

set_api(API)

ATTACKABLES = [
    API.Notoriety.Gray,
    API.Notoriety.Criminal,
    API.Notoriety.Enemy,
    API.Notoriety.Murderer,
]
RANGE = 5


@trap_errors
def attack_closest():
    valid_targets = get_mobs_by(ATTACKABLES, RANGE)

    if not valid_targets:
        API.SysMsg("No valid attackable / hostiles found.")
        return

    valid_targets.sort(key=lambda m: m.Distance)
    closest_mob = valid_targets[0]

    noto_log = str(closest_mob.Notoriety)
    API.SysMsg(f"Engaging {noto_log} target at distance {closest_mob.Distance}")

    API.Attack(closest_mob.Serial)


attack_closest()
