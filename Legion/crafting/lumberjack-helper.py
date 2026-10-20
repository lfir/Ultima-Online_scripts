import API
from _utils import set_api, trap_errors, wait_for_target

# Need to manually move from tree to tree and select each tree once.
# "BoardsToLlama" organizer required to move boards to a pack animal when inventory is full.

# --- Configuration ---
AXE_SERIAL = 1109668282
LOG_GRAPHIC = 0x1BDD
BOARD_GRAPHIC = 0x1BD7

set_api(API)


@trap_errors
def process_and_stash_wood():
    """Cuts all log stacks into boards and defers to the Organizer agent for stashing."""
    # Fetch every stack of logs currently in the backpack
    log_stacks = API.FindTypeAll(LOG_GRAPHIC, API.Player.Backpack.Serial)

    if log_stacks:
        API.SysMsg("Logs found. Chopping all stacks...", 52)

        for logs in log_stacks:
            # Always check the stop flag during iterations
            if API.StopRequested:
                break

            API.UseObject(AXE_SERIAL)

            if wait_for_target():
                API.Target(logs.Serial)
                # Pause to allow the server to process the crafting action before the next loop
                API.Pause(1.0)
            else:
                API.SysMsg(
                    "Error: Axe failed to produce a cursor. Halting chopping.", 33
                )
                break

    # After all logs are processed, check for boards and trigger Organizer
    boards = API.FindType(BOARD_GRAPHIC, API.Player.Backpack.Serial)

    if boards:
        API.SysMsg("Running Organizer: BoardsToLlama...", 52)
        API.Organizer("BoardsToLlama")
        # Wait for the organizer to process the drag/drop queue
        API.Pause(1.0)


def chop_tree():
    """Handles the user prompt, manual target, and auto-chopping loop."""
    API.SysMsg("=== CLICK ON A TREE TO START ===", 52)
    API.UseObject(AXE_SERIAL)

    if wait_for_target():
        API.SysMsg("Awaiting your manual click...", 52)
        while API.HasTarget() and not API.StopRequested:
            API.Pause(0.1)

    target_pos = API.LastTargetPos
    target_graphic = API.LastTargetGraphic

    if not target_pos or not target_graphic:
        API.SysMsg("Error: Invalid static target captured.", 33)
        return

    x = int(target_pos.X)
    y = int(target_pos.Y)
    z = int(target_pos.Z)
    graphic = int(target_graphic)

    API.SysMsg("Tree locked. Auto-chopping until empty...", 52)

    while not API.StopRequested:
        API.ClearJournal()
        API.UseObject(AXE_SERIAL)

        if wait_for_target():
            API.Target(x, y, z, graphic)

        timeout = 50
        action_complete = False
        tree_empty = False

        while timeout > 0 and not API.StopRequested:
            if API.InJournalAny(
                ["not enough wood", "too far away", "can't use", "cannot be harvested"]
            ):
                tree_empty = True
                action_complete = True
                break

            if API.InJournalAny(
                ["You put some", "fail to produce", "hack at the tree"]
            ):
                action_complete = True
                break

            API.Pause(0.1)
            timeout -= 1

        if tree_empty:
            API.SysMsg("Tree is empty! Processing inventory...", 52)
            break

        if not action_complete:
            API.SysMsg("Chop timeout. Retrying swing...", 52)


# --- Main Execution ---
API.SysMsg("TazUO Lumberjack Helper Initialized...", 52)

while not API.StopRequested:
    chop_tree()
    process_and_stash_wood()
    API.Pause(0.5)
