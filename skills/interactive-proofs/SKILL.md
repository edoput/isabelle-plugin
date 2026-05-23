---
name: interactive-proofs
description: Use when asked to develop a proof interactively in Isabelle.
---

# Prerequisites

This skill requires the Isabelle MCP (AKA I/Q) to be available and the `explore` command to be enabled. Warn the user that
they need to import the Isar_Explore theory if it's not available.

## Interactive proofs

Interactive proofs are a loop of `explore` and `get_command_info` that work at the cursor. A successful tactic application will change the goal and move the cursor after the tactic.
For interactive proofs you only use apply style and structure it using subgoals. Stop working in apply style after 10 iterations of the loop and report to the user the current proof structure and what goals it relates to.

# Examples

## apply auto

This will use the tactic auto and you will get back the results of using the tactic on the current goal.
auto is a LIFO tactic, the last goal is processed first

```
- explore query: proof, command_selection: current, arguments: apply auto
- get_command_info mode: current, include_results: true
```

## apply simp

This will use the tactic simp and you will get back the results of using the tactic on the current goal.
The simplifier rewrites goals and assumptions using rewrite rules of the form ?LHS = ?RHS. The rewrite
direction is always from ?LHS to ?RHS. The simplifier 

```
- explore query: proof, command_selection: current, arguments: apply simp
- get_command_info mode: current, include_results: true
```

The simp tactic accepts named arguments, e.g.

- add: identifier, e.g. add: algebra_simps adds the algebra_simps theorem collection
- del: identifier, e.g. del: iffy_rewrite_rule remove the iffy_rewrite_rule from the simpset

You can mix and match the arguments

```
- explore query: proof, command_selection: current, arguments: apply (simp add: algebra_simps del: some_bad_theorem)
```

## sledgehammer

Sledgehammer only returns valid proofs from automatic theorem provers or "no proof found".

```
- explore query: sledgehammer, command_selection: current
```

Prefer the ones with the lowest time reported. You replace the sledgehammer command with the proof found by the ATPs.
E.g. sledgehammer returns the following and you choose the one from cvc5 because it is tagged as taking 48ms to check.

```
- cvc5 (48 ms): by (meson A wsim.simps)
- zipperposition (111 ms): by (meson A wsim.cases wsim_diverge)
```
