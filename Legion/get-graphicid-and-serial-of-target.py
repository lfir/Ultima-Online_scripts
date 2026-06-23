import API
from _utils import trap_errors


@trap_errors
def get_serial():
    API.SysMsg("Select any object on screen (Mobile, Item, or Static)...", 52)

    # RequestAnyTarget returns an ApiGameObject directly
    target_entity = API.RequestAnyTarget(10)

    if target_entity:
        try:
            name = getattr(target_entity, "Name", "Unknown")
            serial = getattr(target_entity, "Serial", -1)
            graphic = getattr(target_entity, "Graphic", -1)

            msg = f"Name: {name} | Serial: {serial} | Graphic: {graphic}"

            API.SysMsg(msg, 52)
        except Exception as e:
            API.SysMsg(f"Error reading entity: {e}", 33)
    else:
        API.SysMsg("Targeting cancelled or timed out.", 33)


get_serial()
