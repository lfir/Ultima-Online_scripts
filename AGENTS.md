# AI Agent Instructions

This repository contains python scripting resources for Ultima Online, specifically using the TazUO client and the Legion API.

## Reference Documentation

Always refer to the following documentation sites when working in this repository:

### TazUO & Legion Python Scripting

- Use these as the primary references for writing, modifying, and debugging scripts:
  - [TazUO Wiki](https://tazuo.org/wiki/home/)
  - [Legion API Reference](https://tazuo.org/legion/legionapi/)

### UOAlive Server Mechanics

- Use this reference when evaluating server-specific mechanics, rules, custom systems, and behavior for the UOAlive free shard:
  - [UOAlive Wiki](https://uoalive.com/wiki/UOA)

### Example Code

- External examples of existing scripts can be found at [PlayTazUO/PublicLegionScripts](https://github.com/PlayTazUO/PublicLegionScripts).

## Scripting Best Practices

- **Logging State:** Always include descriptive `API.SysMsg()` logs throughout scripts so the user knows exactly what state the script is in at all times.
- **Error Handling:** Uncaught exceptions must be avoided as the client does not handle them gracefully. Always catch exceptions and output the error using `API.SysMsg()` with color code `33` (red) (e.g., `API.SysMsg("No valid attackable / hostiles found.", 33)`).
- **Main entry point of the script:** NEVER include `if __name__ == "__main__":`.
