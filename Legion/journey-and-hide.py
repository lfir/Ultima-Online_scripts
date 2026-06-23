import API

# --- CONFIGURATION ---
WIN_W = 310
ROW_H = 30
HEADER_H = 42
COL_HDR_H = 20
MAX_VISIBLE_ROWS = 6
# Time to wait after triggering Sacred Journey before hiding (Cast time + Server transition).
# Adjust as needed.
TELEPORT_DELAY_SECONDS = 2
# ---------------------


def _use_runebook_and_wait(book_serial):
    """Safely opens the runebook and waits for the gump using a timeout loop."""
    API.UseObject(book_serial)

    timeout_loops = 30
    while not API.HasGump() and timeout_loops > 0 and not API.StopRequested:
        API.Pause(0.1)
        timeout_loops -= 1


def journey_and_hide(rune_num, book_serial):
    """Executes Sacred Journey, waits for the teleport, and immediately hides."""

    # 1. Strict Mana & Tithing Check
    # Sacred Journey requires 15 Mana and 15 Tithing Points.
    if API.Player.TithingPoints < 15:
        API.SysMsg("Not enough Tithing Points for Sacred Journey!", 33)
        return

    if API.Player.Mana < 15:
        API.SysMsg("Not enough Mana for Sacred Journey!", 33)
        return

    if API.StopRequested:
        return

    # 2. Open the book natively so the server registers the gump
    _use_runebook_and_wait(book_serial)

    if not API.HasGump():
        API.SysMsg("Error: Runebook gump failed to open.", 33)
        return

    # 3. Trigger Sacred Journey
    # The default runebook index page buttons for Sacred Journey map to 75 through 90.
    # 75 is slot 0 (default), 76 is slot 1, etc.
    button_id = 75 + rune_num
    API.ReplyGump(button_id)
    API.SysMsg("Casting Sacred Journey... Queuing Hide skill.", 52)

    # 4. Wait for the spell and teleport to complete
    wait_loops = int(TELEPORT_DELAY_SECONDS * 10)
    while wait_loops > 0 and not API.StopRequested:
        API.Pause(0.1)
        wait_loops -= 1

    if not API.StopRequested:
        API.UseSkill("Hiding")
        API.SysMsg("Hide executed.", 66)


def parse_rune_names(raw_text):
    """Parses the PacketGumpText to extract valid rune names."""
    lines = [l.strip() for l in raw_text.split("\n")]
    runes = []

    for i in range(16):
        idx = 2 + i
        if idx < len(lines):
            name = lines[idx]
            if name and name.lower() != "empty":
                runes.append((i, name))

    return runes


def build_ui(runes, book_serial):
    """Constructs the custom Gump interface."""
    visible_rows = min(len(runes), MAX_VISIBLE_ROWS)
    scroll_h = visible_rows * ROW_H
    win_h = HEADER_H + COL_HDR_H + scroll_h + 8

    gump = API.Gumps.CreateGump(keepOpen=True)
    gump.SetWidth(WIN_W)
    gump.SetHeight(win_h)
    gump.CenterXInViewPort()
    gump.CenterYInViewPort()

    # Background
    bg = API.Gumps.CreateGumpColorBox(0.88, "#111827")
    bg.SetWidth(WIN_W)
    bg.SetHeight(win_h)
    gump.Add(bg)

    # Header bar
    header_bg = API.Gumps.CreateGumpColorBox(0.95, "#1E3A5F")
    header_bg.SetRect(0, 0, WIN_W, HEADER_H)
    gump.Add(header_bg)

    title_lbl = API.Gumps.CreateGumpTTFLabel("Safe Chiv Travel UI", 16, "#A8D8FF")
    title_lbl.SetPos(10, 12)
    gump.Add(title_lbl)

    # Column headers
    col_header_bg = API.Gumps.CreateGumpColorBox(0.7, "#0D2137")
    col_header_bg.SetRect(0, HEADER_H, WIN_W, COL_HDR_H)
    gump.Add(col_header_bg)

    name_hdr = API.Gumps.CreateGumpTTFLabel("Destination", 11, "#88AACC")
    name_hdr.SetPos(10, HEADER_H + 3)
    gump.Add(name_hdr)

    # Scroll area
    scroll = API.Gumps.CreateGumpScrollArea(0, HEADER_H + COL_HDR_H, WIN_W, scroll_h)
    gump.Add(scroll)

    for i, (slot, name) in enumerate(runes):
        y = i * ROW_H

        # Alternating row background
        row_color = "#162032" if i % 2 == 0 else "#0F1922"
        row_bg = API.Gumps.CreateGumpColorBox(0.65, row_color)
        row_bg.SetRect(0, y, WIN_W - 16, ROW_H - 1)
        scroll.Add(row_bg)

        # Rune name
        lbl = API.Gumps.CreateGumpTTFLabel(name, 13, "#E0E8FF")
        lbl.SetPos(10, y + 7)
        scroll.Add(lbl)

        # Safe Sacred Journey button
        rb = API.Gumps.CreateSimpleButton("Go", 100, 22)
        rb.SetPos(180, y + 4)
        scroll.Add(rb)

        # Bind the click event safely using a default argument lambda
        API.Gumps.AddControlOnClick(rb, lambda s=slot: journey_and_hide(s, book_serial))

    API.Gumps.AddGump(gump)

    return gump


# --- ENTRY POINT ---
API.SysMsg("Target your Runebook to generate the Safe Travel UI...", 52)
target_serial = API.RequestTarget(30)

if not target_serial:
    API.SysMsg("Targeting cancelled or timed out.", 33)
else:
    _use_runebook_and_wait(target_serial)

    if not API.HasGump():
        API.SysMsg("Failed to read Runebook. Are you sure that was a runebook?", 33)
    else:
        # 2. Extract names and close the native gump
        gump_data = API.GetGump()
        raw_text = gump_data.PacketGumpText
        valid_runes = parse_rune_names(raw_text)

        API.CloseGump()
        API.Pause(0.15)

        if not valid_runes:
            API.SysMsg("No named runes found in this book.", 33)
        else:
            # 3. Build the persistent custom UI
            ui_gump = build_ui(valid_runes, target_serial)
            API.SysMsg("Safe Travel UI generated.", 66)

            # Keep the script alive so the UI buttons function
            while not API.StopRequested and not ui_gump.IsDisposed:
                API.ProcessCallbacks()
                API.Pause(0.25)
