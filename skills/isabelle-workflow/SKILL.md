---
name: isabelle-workflow
description: Use when working with Isabelle/HOL. Describes when to use tools from the MCP. 
---

# Workflow

Before searching for a definition or theorem, use the find-in-isabelle skill.

# Working without the filesystem

Only interact with theory files using the MCP server. Theory files are not always available in the filesystem because of how import statement works. They may come from the HOL library or the AFP which is not available on the filesystem you have access to.

When a file accesible from the MCP shows the old content after an edit, stop and ask the user.

# Working with Isabelle via the MCP

The MCP includes the following tools for you to use.

## File manipulation

A session includes files and their transitive dependencies. Most likely the session is already started and contains the full files you need but you can manipulate these. The user has also access to these files in the JEdit window. You can ask the user anything about these files.

- `list_files` — Use in place of `ls`. Lists all files tracked by Isabelle in the current session. This inlcudes the full hierarchy and their open/closed state.
- `open_file` — Open a file before reading and writing to it.
- `create_file` — Create a new file only if prompted by the user.
- `read_file` — Reading and searching through an open file.
- `write_file` — Writing to an open theory file, returns outcome of writing on the theory commands.
- `save_file` — Persists files to disk.

## Theory manipulation

You can manipulate a theory in memory without manipulating the file. The user will not see these changes. There is a notion of a current command, a cursor into an open theory. Isabelle processes all commands before the cursor.

- `explore` — When working on a proof use explore, this will run the commands you want in memory at the current cursor. Can be scoped to manipulate the cursor. See the proof-exploration skills.
- `get_command_info` — When working, get information about the theory and proof context at the cursor or for a specific range. See the isabelle-verify skill.
