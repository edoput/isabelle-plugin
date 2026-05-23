---
name: isabelle-workflow
description: Use when working with Isabelle/HOL. Describes how to get
  errors warnings. Describes how to develop proofs. Describes using tactics
  in interactive mode and using automation successfully.
---

# Working without the filesystem

Only interact with theory files using the MCP server. Theory files are not always available in the filesystem because of how import statement works. They may come from the HOL library or the AFP which is not available on the filesystem you have access to.

# Working with Isabelle via the MCP

The MCP includes the following tools for you to use. Theory files are a sequence of commands for specifications (definition, (co)inductive, (co)datatype, lemma, theorem, ...) and a sequence of commands for proofs (apply, sledgehammer, ...). The commands are processed
sequentially and their outcome is sensitive to the order of definitions in the files.

### File manipulation

A session includes files and their transitive dependencies. Most likely the session is already started and contains the full files you need but you can manipulate these.
The user has also access to these files in the JEdit window. You can ask the user anything about these files.

- `list_files` — Use in place of `ls`. Lists all files tracked by Isabelle in the current session. This inlcudes the full hierarchy and their open/closed state.
- `open_file` — Open a file before reasing and writing to it.
- `create_file` — Create a new file only if prompted by the user.
- `read_file` — Reading and searching through an open file.
- `write_file` — Writing to an open theory file, returns outcome of writing on the theory commands.
- `save_file` — Persists files to disk.

### Theory manipulation

You can manipulate a theory in memory without manipulating the file. The user will not see these changes. There is a notion of a current command, a cursor into an open theory. Isabelle processes all commands before the cursor.

- `explore` — When working on a proof use explore, this will run the commands you want in memory at the current cursor. Can be scoped to manipulate the cursor.
- `get_command_info` — When working, get information about the theory and proof context at the cursor or for a specific range.
- `get_document_info` — When starting and finishing make sure all command status across a theory are successful.

## Diagnostics workflow

Only use `get_document_info` with `include_results=false` and `xml_result_file` pointing to a known path. 

```
get_command_info(
    mode       = 'line',
    path       = '/path/to/Theory.thy',
    start_line = 1,
    end_line   = -1,
    include_results  = false,
    xml_result_file  = '/path/to/Theory_diag.xml'
)
```

The MCP response contains a path to the JSON result file (e.g. `/tmp/isabelle-results-XXXX.json`).  If the response is too large it is automatically saved as an overflow file and the path is shown in the tool result.

The postprocess it using the diagnostic script.

```bash
python3 /path/to/.claude/skills/isabelle-workflow/diag.py <result.json> --xml <Theory_diag.xml>
```

## Interactive proofs

Interactive proofs are a loop of `explore` and `get_command_info` that work at the cursor. A successful tactic application will change the goal and move the cursor after the tactic.
For interactive proofs you only use apply style and structure it using subgoals. Stop working in apply style after 10 iterations of the loop.

Example

```
- explore query: proof, command_selection: current, arguments: apply auto
- get_command_info mode: current, include_results: true
```

This will use the tactic auto and you will get back the results of using the tactic on the current goal.

Example

```
- explore query: proof, command_selection: current, arguments: apply auto
- get_command_info mode: current, include_results: true
- explore query: sledgehammer, command_selection: current
```

This will run the tactic auto, and after reading the current goal you try to use sledgeahmmer.
Sledgehammer only returns valid proofs from ATPs. Prefer the ones with the lowest time reported. 
You replace the sledgehammer command with the proof found by the ATPs.

E.g. sledgehammer returns the following and you choose the one from cvc5 because it is tagged as taking 48ms to check.

```
- cvc5 (48 ms): by (meson A wsim.simps)
- zipperposition (111 ms): by (meson A wsim.cases wsim_diverge)
```
