---
name: find-in-isabelle
description: Use before searching for a definition or a theorem in Isabelle. Covers usage of tool read_file in Search mode for locating definitions (datatype, fun, coinductive, etc.) and tool find_theorems for locating lemmas by name or term shape.
---

# Definitions

Search for a definition using `read_file` in Search mode. The following commands introduce names
and are considered definitions: datatype, codatatype, definition, abbreviation, inductive, coinductive,
fun, primrec, primcorec, corec. To search against these commands use the following tool calls.

```json
{
    "path": "<TheoryFile.thy>",
    "mode": "Search",
    "pattern": "datatype.*<name>",
    "context_lines": 5
}
{
    "path": "<TheoryFile.thy>",
    "mode": "Search",
    "pattern": "codatatype.*<name>",
    "context_lines": 5
}
{
    "path": "<TheoryFile.thy>",
    "mode": "Search",
    "pattern": "definition <name>",
    "context_lines": 5
}
{
    "path": "<TheoryFile.thy>",
    "mode": "Search",
    "pattern": "abbreviation <name>",
    "context_lines": 5
}
{
    "path": "<TheoryFile.thy>",
    "mode": "Search",
    "pattern": "inductive <name>",
    "context_lines": 5
}
{
    "path": "<TheoryFile.thy>",
    "mode": "Search",
    "pattern": "coinductive <name>",
    "context_lines": 5
}
{
    "path": "<TheoryFile.thy>",
    "mode": "Search",
    "pattern": "fun <name>",
    "context_lines": 5
}
{
    "path": "<TheoryFile.thy>",
    "mode": "Search",
    "pattern": "primrec <name>",
    "context_lines": 5
}
{
    "path": "<TheoryFile.thy>",
    "mode": "Search",
    "pattern": "primcorec <name>",
    "context_lines": 5
}
{
    "path": "<TheoryFile.thy>",
    "mode": "Search",
    "pattern": "corec <name>",
    "context_lines": 5
}
```

<examples>
  <example index="1">
  <call>
  {
      "path": "traces.thy",
      "mode": "Search",
      "pattern": "codatatype.*ctrace",
      "context_lines": 4
  }
  </call>
  <output>
  /path/to/traces.thy-11-  - infinite activity
  /path/to/traces.thy-12-  - termination
  /path/to/traces.thy-13-  - divergence
  /path/to/traces.thy-14-*)
  /path/to/traces.thy:15:codatatype ('e, 's) ctrace =
  /path/to/traces.thy-16-  is_TCons : TCons 'e "('e, 's) ctrace" |
  /path/to/traces.thy-17-  is_Term : Term 's |
  /path/to/traces.thy-18-  is_Div : Div
  /path/to/traces.thy-19-
  </output>
  <commentary>
  Search against content of traces.thy for a line matching the regex codatatype.*ctrace . Inlcudes 4 lines before and after line match. The output lists the content of traces.thy that contains the matching line codatatype ('e, 's) ctrace. 
  </commentary>
</example>
<example index="2">
  <call>
  {
      "path": "traces.thy",
      "mode": "Search",
      "pattern": "coinductive ctrace_of",
      "context_lines": 10
  }
  </call>
  <output>
  /path/to/traces.thy-18-  is_Div : Div
  /path/to/traces.thy-19-
  /path/to/traces.thy-20-lemma is_TConsE [elim]:
  /path/to/traces.thy-21-  "⟦ is_TCons tr; ⋀ e tr'. tr = TCons e tr' ⟹ Q⟧ ⟹ Q"
  /path/to/traces.thy-22-  by (metis is_TCons_def)
  /path/to/traces.thy-23-
  /path/to/traces.thy-24-lemma is_TermE [elim]:
  /path/to/traces.thy-25-  "⟦ is_Term tr; ⋀ x. tr = Term x ⟹ Q⟧ ⟹ Q"
  /path/to/traces.thy-26-  by (metis is_Term_def)
  /path/to/traces.thy-27-
  /path/to/traces.thy:28:coinductive ctrace_of :: "('e, 's, 'b) ctree ⇒ ('e, 's) ctrace ⇒ bool"
  /path/to/traces.thy-29-  where
  /path/to/traces.thy-30-trace_of_RetI [intro]: "ctrace_of (Ret x) (Term x)" |
  /path/to/traces.thy-31-― ‹implies that the equation P = τ P will give use ‹Div›? Yes because we are doing a gp construction.›
  /path/to/traces.thy-32-trace_of_SilI [intro]: "ctrace_of P t ⟹ ctrace_of (τ P) t" |
  /path/to/traces.thy-33-― ‹This allows for nondeterministic choice which makes it a relation.›
  /path/to/traces.thy-34-trace_of_VisI [intro]: "⟦ ∃ P ∈⇩b (K e). ctrace_of P t ⟧⟹ ctrace_of (Vis K) (TCons e t)"
  /path/to/traces.thy-35-monos bBex_mono
  /path/to/traces.thy-36-
  /path/to/traces.thy-37-lemma ctrace_of_coind [elim, consumes 1, case_names Ret Sil Vis, induct pred: "ctrace_of"]:
  /path/to/traces.thy-38-  assumes major: "φ P tr"
  </output>
  <commentary>
  Search against content of traces.thy for a line matching the string coinductive ctrace_of . Includes 10 lines before and after line match. The output lists the content of traces.thy that contains the matching line coinductive ctrace_of .
  </commentary>
  </example>
</examples>

# Theorems

Find lemmas using the `explore` tool. There are two ways to search lemmas, by name or by term.

## Search theorems by name

You can search a theorem by substring match on the theorem name. Multiple names are AND-ed -- all patterns must appear in the name.

```json
{
    "query": "find_theorems",
    "command_selection": "current",
    "arguments": "name: <name1>"
}
```

Theorem names are predictable, they will contain the names of the constants they use.

<examples>
  <example index="1">
    <document>
      <source>traces.thy</source>
      <document_content>
        lemma ctrace_of_diverge [simp]:
          "ctrace_of diverge anything"
        
        lemma ctrace_of_magic_iff [iff]:
          "ctrace_of magic x <--> False"
      </document_content>
    </document>
    <call>
    {
        "query": "find_theorems",
        "command_selection": "current",
        "arguments": "name: ctrace_of name: diverge"
    }
    </call>
    <output>
    find_theorems 'name: ctrace_of name: diverge': 2 theorem(s) found (2 displayed)
           name: "ctrace_of"
           name: "diverge"
           traces.ctrace_of_diverge: ctrace_of diverge ?anything
           traces.ctrace_of_all_diverge: (∀tr. ctrace_of ?P tr) = (?P = diverge)
    
         Full results saved to explore.json
    </output>
  </example>

  <example index="2">
    <document>
      <source>traces.thy</source>
      <document_content>
      lemma ctrace_of_diverge [simp]:
        "ctrace_of diverge anything"
      
      lemma ctrace_of_magic_iff [iff]:
        "ctrace_of magic x <--> False"
      </document_content>
    </document>
    <call>
    {
        "query": "find_theorems",
        "command_selection": "current",
        "arguments": "name: ctrace_of name: magic"
    }
    </call>
    <output>
    find_theorems 'name: ctrace_of name: magic': 2 theorem(s) found (2 displayed)
           name: "ctrace_of"
           name: "magic"
           refinement.ctrace_of_magic_iff: ctrace_of magic ?anything = False
           refinement.ctrace_of_more_magic: ctrace_of more_magic ?anything = False
    
         Full results saved to explore.json
    </output>
    <commentary>
    Search for a theorem by name. The theorem name must match both ctrace_of and magic.
    </commentary>
  </example>
</examples>

## Search theorems by term

You search by term shape as follows. The term shape is always enclosed within a cartouche pair \<open>...\<close>.

```json
{
    "query": "find_theorems",
    "command_selection": "current",
    "arguments": "\<open><term_shape>\<close>"
}
```

The term shape

1. constant identifiers are used as is
   <example>
   <call>
   {
       "query": "find_theorems",
       "command_selection": "current",
       "arguments": "\<open>ctrace_of diverge Div\<close>"
   }
   </call>
   <output>
find_theorems '\<open>ctrace_of diverge Div\<close>': 1 theorem(s) found (1 displayed)
       ctree_simon_refinement.ctrace_of_diverge_Div: ctrace_of diverge Div

     Full results saved to explore.json
   </output>
   <commentary>
   Search for a theorem matching the term ctrace_of diverge Div . Unbound identifiers never match.
   </commentary>
   </example>
2. Any term can be replaced by the placeholder token `_` to generalize the theorem.
   <example>
   <call>
   {
       "query": "find_theorems",
       "command_selection": "current",
       "arguments": "\<open>ctrace_of diverge _\<close>"
   }
   </call>
   <output>
find_theorems '\<open>ctrace_of diverge _\<close>': 1 theorem(s) found (1 displayed)
     ctree_simon_traces.ctrace_of_diverge: ctrace_of diverge ?anything

     Full results saved to explore.json
   </output>
   <commentary>
   Search for any theorem matching the term ctrace_of diverge _ . This example uses the placeholder _ in place of an indentifier to generalize the theorem statement.
   </commentary>
   </example>
3. Any valid term construction is accepted, even the ones containing placeholders.
   <example>
   <call>
   {
       "query": "find_theorems",
       "command_selection": "current",
       "arguments": "\<open>ctrace_of (Sil _) _\<close>"
   }
   </call>
   <output>
find_theorems '\<open>ctrace_of (Sil _) _\<close>': 2 theorem(s) found (2 displayed)
       ctree_simon_traces.ctrace_of_Sil: ctrace_of (τ ?P) ?t = ctrace_of ?P ?t
       ctree_simon_traces.ctrace_of.trace_of_SilI: ctrace_of ?P ?t ⟹  ctrace_of (τ ?P) ?t

     Full results saved to explore.json
   </output>
   <commentary>
   Search for a theorem matching the term ctrace_of (Sil _) _ . Arbitrary terms can be constructed using uthe placeholder _
   </commentary>
   </example>
4. use schematic variables ?x when you want a reusable placeholder
   <example>
   <call>
   {
       "query": "find_theorems",
       "command_selection": "current",
       "arguments": "\<open>?x + ?y = ?x\<close>"
   }
   </call>
   <output>
find_theorems '\<open>?x + ?y = ?x\<close>': 11 theorem(s) found (11 displayed)
       Groups.monoid_add_class.add_0_right: ?a + 0 = ?a
       Semiring_Normalization.comm_semiring_1_class.semiring_normalization_rules(6): ?a + 0 = ?a
       Groups.comm_monoid_add_class.add.comm_neutral: ?a + 0 = ?a
       SMT.verit_sum_simplify: ?a + 0 = ?a
       Int.plus_int_code(1): ?k + 0 = ?k
       SMT.z3_rule(114): ?x + 0 = ?x
       Nat.add_0_right: ?m + 0 = ?m
       String.add_literal_code(2): ?s + STR '''' = ?s
       Code_Numeral.plus_integer_code(1): ?k + 0 = ?k
       Groups.cancel_comm_monoid_add_class.add_cancel_left_right: (?a + ?b = ?a) = (?b = 0)
       Nat.add_eq_self_zero: ?m + ?n = ?m ⟹ ?n = 0

     Full results saved to explore.json
   </output>
   <commentary>
   Search for any theorem matching the term ?x + ?x = ?x . This example uses the named placeholder ?x in place of an identifier. This term shape will not match unless the subterm matched by ?x is the same everywhere.
   </commentary>
   </example>
   <example>
   <call>
   {
       "query": "find_theorems",
       "command_selection": "current",
       "arguments": "\<open>?x - ?y = 0\<close>"
   }
   </call>
   <output>
find_theorems '\<open>?x - ?y = 0\<close>': 15 theorem(s) found (15 displayed)
       Num.neg_numeral_class.diff_numeral_special(9): 1 - 1 = 0
       Groups.group_add_class.diff_self: ?a - ?a = 0
       Groups.comm_monoid_diff_class.zero_diff: 0 - ?a = 0
       Groups.cancel_comm_monoid_add_class.diff_cancel: ?a - ?a = 0
       Nat.diff_0_eq_0: 0 - ?n = 0
       Nat.diff_self_eq_0: ?m - ?m = 0
       Code_Numeral.natural_zero_minus_one: 0 - 1 = 0
       Num.neg_numeral_class.diff_numeral_special(12): - 1 - - 1 = 0
       Groups.comm_monoid_diff_class.diff_add_zero: ?a - (?a + ?b) = 0
       Nat.diff_add_0: ?n - (?n + ?m) = 0
       Groups.group_add_class.eq_iff_diff_eq_0: (?a = ?b) = (?a - ?b = 0)
       Groups.group_add_class.right_minus_eq: (?a - ?b = 0) = (?a = ?b)
       Nat.diff_is_0_eq: (?m - ?n = 0) = (?m ≤ ?n)
       Nat.diff_is_0_eq': ?m ≤ ?n ⟹ ?m - ?n = 0
       Nat.diffs0_imp_equal: ?m - ?n = 0 ⟹ ?n - ?m = 0 ⟹ ?m = ?n

     Full results saved to explore.json
   </output>
   <commentary>
   Search for any theorem matching the term ?x - ?y = 0. This example uses the named placeholders ?x and ?y in place of an identifier. This term shape will match when the subterms matched by ?x and ?y are different.
   </commentary>
   </example>

## Generalize

When searching by term generalize the theorem statement.

<example>
   <call>
   {
       "query": "find_theorems",
       "command_selection": "current",
       "arguments": "\<open>ctrace_of diverge _\<close>"
   }
   </call>
   <output>
find_theorems '\<open>ctrace_of diverge Div\<close>': 1 theorem(s) found (1 displayed)
       ctree_simon_refinement.ctrace_of_diverge: ctrace_of diverge ?anything

     Full results saved to explore.json
   </output>
   <commentary>
   Instead of searching for ctrace_of diverge Div, generalize to ctrace_of diverge _ . The term ctrace_of diverge Div is too specific to be a reasonable theorem already proved.
   </commentary>
   </example>
</example>

## find_theorems is context sensitive

explore is context dependent. Changing the command_selection parameter will change the output of the tool for both search by name and search by term.

<examples>
  <document>
    <source>traces.thy</source>
    <document_content>
    lemma ctrace_of_diverge [simp]:
      "ctrace_of diverge anything"
    
    lemma ctrace_of_magic_iff [iff]:
      "ctrace_of magic x <--> False"

    lemma ctrace_of_more_magic_iff [iff]:
      "ctrace_of more_magic x <--> False"
    </document_content>
  </document>
  <example index="1">
    <call>
    {
        "query": "find_theorems",
        "command_selection": "file_pattern",
        "path": "traces.thy",
        "pattern":  "lemma ctrace_of_diverge",
        "arguments": "\<open>ctrace_of magic _\<close>"
    }
    </call>
    <output>
find_theorems '\<open>ctrace_of magic _\<close>': 0 theorem(s) found (0 displayed)
     No theorems found.

     Full results saved to explore.json
    </output>
    <commentary>
The find_theorems call happens at the ctrace_of_diverge lemma. This means that ctrace_of_magic_iff is not processed yet and cannot be found.
    </commentary>
  </example>
  <example index="2">
    <call>
    {
        "query": "find_theorems",
        "command_selection": "file_pattern",
        "path": "traces.thy",
        "pattern":  "lemma ctrace_of_more_magic",
        "arguments": "\<open>ctrace_of magic _\<close>"
    }
    </call>
    <output>
find_theorems '\<open>ctrace_of magic _\<close>': 1 theorem(s) found (1 displayed)
     traces.ctrace_of_magic_iff: ctrace_of magic ?x <--> False

     Full results saved to explore.json
    </output>
    <commentary>
The find_theorems call happens at the ctrace_of_more_magic lemma. This means that ctrace_of_magic_iff is processed yet and can be found.
    </commentary>
  </example>
<examples>
