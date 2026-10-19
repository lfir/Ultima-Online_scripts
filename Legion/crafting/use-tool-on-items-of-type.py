import API
from _utils import set_api, wait_for_target

set_api(API)

API.SysMsg("Target the tool you want to use...", 52)
tool_serial = API.RequestTarget()

API.SysMsg("Target an item of the type you want to process...", 52)
sample_item_serial = API.RequestTarget()

# Retrieve the sample item object to get its Graphic ID
sample_item = API.FindItem(sample_item_serial)

if sample_item:
    target_graphic = sample_item.Graphic
    API.SysMsg(
        f"Identified Graphic ID: {target_graphic}. Processing backpack items...", 52
    )

    # Locate all matching items in the backpack
    items_to_process = API.FindTypeAll(target_graphic, API.Backpack)

    for item in items_to_process:
        if API.StopRequested:
            break

        # Double-click the tool
        API.UseObject(tool_serial)

        # Apply target if cursor is present
        if wait_for_target():
            API.Target(item.Serial)
            API.Pause(0.5)  # Pace execution for server synchronization

    API.SysMsg("Processing complete.", 52)
