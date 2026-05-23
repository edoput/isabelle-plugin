#!/usr/bin/env python3
"""
Isabelle diagnostic filter.

Reads the JSON result file produced by get_command_info and prints a compact
structured report.  Optionally also reads the XML markup file (saved via the
xml_result_file parameter) to enrich error and warning messages when
results_text is absent (i.e. produced with include_results=false).

Usage:
    python3 diag.py <result.json> [--xml <markup.xml>]

Where:
  result.json  — path returned by get_command_info (include_results=false)
                 OR the overflow file Claude Code saves when the response
                 exceeds the token limit.
  markup.xml   — optional; file saved via the xml_result_file parameter.
                 Provides error/warning text when result.json has no
                 results_text.

Each entry includes the source line number so you can navigate back with:
    get_command_info(mode='line', path=..., start_line=N, end_line=N,
                     include_results=True)
"""
import argparse
import html
import json
import re
import sys
import textwrap
import xml.etree.ElementTree as ET


# ── helpers ──────────────────────────────────────────────────────────────────

def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def first_line(s: str) -> str:
    return s.strip().splitlines()[0] if s.strip() else ""


WARNING_PATTERNS = (
    "Ignoring duplicate rewrite rule",
    "Ignoring duplicate introduction",
    "Introduced fixed type variable",
)


# ── XML enrichment ────────────────────────────────────────────────────────────

def load_xml_messages(xml_path: str) -> tuple[list[str], list[str]]:
    """
    Parse the markup XML and return two ordered lists of clean text:
      error_texts   — texts from all <error_message> elements, in document order
      warning_texts — texts from all <warning_message> elements, in document order
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    results_el = root.find("results")
    if results_el is None:
        return [], []

    error_texts: list[str] = []
    warning_texts: list[str] = []

    for result in results_el:
        raw = ET.tostring(result, encoding="unicode")
        inner_str = html.unescape(raw)
        inner_str = re.sub(r"^<result[^>]*>", "", inner_str)
        inner_str = re.sub(r"</result>\s*$", "", inner_str)
        try:
            wrapped = ET.fromstring(f"<root>{inner_str}</root>")
        except ET.ParseError:
            continue
        for child in wrapped:
            text = strip_tags(ET.tostring(child, encoding="unicode"))
            if child.tag == "error_message" and text:
                error_texts.append(text)
            elif child.tag == "warning_message" and text:
                warning_texts.append(text)

    return error_texts, warning_texts


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Isabelle diagnostic filter")
    parser.add_argument("result_file", help="JSON result file from get_command_info")
    parser.add_argument("--xml", metavar="MARKUP_XML",
                        help="Optional markup XML from xml_result_file parameter")
    args = parser.parse_args()

    with open(args.result_file) as f:
        data = json.load(f)

    # Optional XML enrichment — collect ordered error/warning texts
    xml_errors: list[str] = []
    xml_warnings: list[str] = []
    if args.xml:
        xml_errors, xml_warnings = load_xml_messages(args.xml)

    cmds = data.get("content", [])
    summary = data.get("summary", {})

    errors: list[dict] = []
    sorries: list[dict] = []
    warnings: list[dict] = []

    warn_xml_idx = 0  # cursor into xml_warnings (warnings appear alongside commands)

    for cmd in cmds:
        status  = cmd.get("status", {}).get("status_summary", "")
        source  = cmd.get("command_source", "").strip()
        line    = cmd.get("range", {}).get("start_line", "?")
        results = cmd.get("results_text") or []

        # ── sorry ────────────────────────────────────────────────────────────
        if source == "sorry":
            sorries.append({"line": line})
            continue

        # ── errors ───────────────────────────────────────────────────────────
        if status == "failed":
            msg = ""
            if results:
                msg = first_line(next((r for r in results if r.strip()), ""))
            if not msg:
                msg = "(see get_command_info for details)"
            errors.append({"line": line, "source": source[:70], "message": msg})

        # ── warnings from results_text ────────────────────────────────────────
        for r in results:
            if any(p in r for p in WARNING_PATTERNS):
                warnings.append({
                    "line":    line,
                    "source":  source[:70],
                    "message": first_line(r)[:200],
                })
                break

    # Enrich errors with XML message text (matched sequentially by order)
    for i, err in enumerate(errors):
        if err["message"] == "(see get_command_info for details)" and i < len(xml_errors):
            err["message"] = first_line(xml_errors[i])[:300]

    # Append XML-only warnings (no results_text available) de-duplicated by message text
    seen_warn_msgs = {w["message"] for w in warnings}
    for xml_w in xml_warnings:
        text = first_line(xml_w)[:200]
        if text and text not in seen_warn_msgs and any(p in xml_w for p in WARNING_PATTERNS):
            warnings.append({"line": "?", "source": "(from XML)", "message": text})
            seen_warn_msgs.add(text)

    # ── report ───────────────────────────────────────────────────────────────
    failed = summary.get("commands_failed", len(errors))
    total  = summary.get("total_commands", len(cmds))

    print(f"Isabelle diagnostics  "
          f"{failed} failed · {len(sorries)} sorry · {len(warnings)} warnings "
          f"(of {total} commands)\n")

    if errors:
        print(f"── ERRORS ({len(errors)}) {'─' * 50}")
        for e in errors:
            print(f"  L{e['line']:>4}  {e['source']!r}")
            for ln in textwrap.wrap(e["message"], 90,
                                    initial_indent="        ",
                                    subsequent_indent="        "):
                print(ln)
        print()

    if sorries:
        print(f"── SORRIES ({len(sorries)}) {'─' * 48}")
        for s in sorries:
            print(f"  L{s['line']:>4}  sorry  ← incomplete proof")
        print()

    if warnings:
        print(f"── WARNINGS ({len(warnings)}) {'─' * 47}")
        for w in warnings:
            print(f"  L{str(w['line']):>4}  {w['source']!r}")
            print(f"        {w['message']}")
        print()

    if not errors and not sorries and not warnings:
        print("No errors, sorries, or warnings found.")

    print("To inspect line N in full:")
    print("  get_command_info(mode='line', path=..., start_line=N, end_line=N, include_results=True)")


if __name__ == "__main__":
    main()
