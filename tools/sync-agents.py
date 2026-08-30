#!/usr/bin/env python3
"""sync-agents.py - generate the opencode variants (.opencode/agent/*.md) from the
Claude Code subagents (.claude/agents/*.md).

The source of truth is always .claude/agents/. After every change there:

    python3 tools/sync-agents.py

Only the frontmatter is translated; the prompt body is copied unchanged.
Differences between the two formats:

  Claude Code            opencode
  ---------------------  ----------------------------------------
  name: <id>             dropped (the file name is the id)
  tools: Read, Bash      tools: {read: true, bash: true, ...}
  model: opus            dropped (the subagent inherits the session model;
                         opencode needs provider/model ids that differ per
                         configured provider)
  color: green           dropped
  -                      mode: subagent
  -                      permission: {edit: deny} for read-only agents

Other agents: some are said to read .claude/agents/ directly (e.g. Cursor),
GitHub Copilot uses .github/agents/*.agent.md - verify against the current
documentation during setup (harness skill, agenten-kompatibilitaet.md) before
adding a target here.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / ".claude" / "agents"
DST_DIR = ROOT / ".opencode" / "agent"

# Claude tool name -> opencode tool name
TOOL_MAP = {
    "read": "read",
    "write": "write",
    "edit": "edit",
    "bash": "bash",
    "grep": "grep",
    "glob": "glob",
    "webfetch": "webfetch",
    "websearch": "webfetch",
    "task": "task",
    "todowrite": "todowrite",
    "todoread": "todoread",
    "ls": "list",
    "list": "list",
}

# All opencode tools that get closed explicitly when a tool list is given
ALL_TOOLS = ["read", "grep", "glob", "list", "bash", "write", "edit", "patch", "webfetch", "task"]


def split_frontmatter(text: str):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError("no YAML frontmatter found")
    return m.group(1), m.group(2).lstrip("\n")


def parse_frontmatter(fm: str) -> dict:
    """Minimal parser: flat key: value pairs plus YAML block scalars (>-, |)."""
    fields, key, buf = {}, None, []
    for line in fm.split("\n"):
        if key and (line.startswith((" ", "\t")) or not line.strip()):
            buf.append(line.strip())
            continue
        if key:
            fields[key] = " ".join(b for b in buf if b).strip()
            key, buf = None, []
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            continue
        name, value = m.group(1), m.group(2).strip()
        if value in (">-", ">", "|", "|-"):
            key = name
        else:
            fields[name] = value.strip("\"'")
    if key:
        fields[key] = " ".join(b for b in buf if b).strip()
    return fields


def build_tools_block(tools_value: str) -> str:
    wanted = set()
    for raw in tools_value.split(","):
        name = raw.strip().lower()
        if name in TOOL_MAP:
            wanted.add(TOOL_MAP[name])
    if not wanted:
        return ""
    # Capabilities without an own tool name in Claude Code that belong to the
    # same class: list belongs to read/glob, patch to edit.
    if {"read", "glob", "grep"} & wanted:
        wanted.add("list")
    if "edit" in wanted:
        wanted.add("patch")
    lines = ["tools:"]
    for tool in ALL_TOOLS:
        lines.append(f"  {tool}: {'true' if tool in wanted else 'false'}")
    return "\n".join(lines) + "\n"


def convert(path: pathlib.Path) -> str:
    fm_text, body = split_frontmatter(path.read_text(encoding="utf-8"))
    fields = parse_frontmatter(fm_text)

    description = fields.get("description", "").replace("\n", " ").strip()
    out = ["---", "description: >-"]
    # Indent the description as a block scalar so special characters do not matter
    for chunk in re.findall(r".{1,90}(?:\s|$)", description):
        out.append("  " + chunk.strip())
    out.append("mode: subagent")

    tools_block = build_tools_block(fields.get("tools", ""))
    if tools_block:
        out.append(tools_block.rstrip("\n"))
        if "  write: false" in tools_block and "  edit: false" in tools_block:
            out.extend(["permission:", "  edit: deny"])
    out.append("---")
    out.append("")
    return "\n".join(out) + "\n" + body


def main() -> int:
    if len(sys.argv) > 1:
        if sys.argv[1] in ("-h", "--help"):
            print(__doc__.strip())
            return 0
        print(f"Unknown argument: {sys.argv[1]}. This tool takes no arguments (see --help).", file=sys.stderr)
        return 2
    if not SRC_DIR.is_dir():
        print(f"Abort: {SRC_DIR} does not exist. Subagents live in .claude/agents/*.md.", file=sys.stderr)
        return 1
    DST_DIR.mkdir(parents=True, exist_ok=True)
    sources = sorted(SRC_DIR.glob("*.md"))
    if not sources:
        print("No agents found in .claude/agents/. Nothing to do.")
        return 0
    for src in sources:
        dst = DST_DIR / src.name
        dst.write_text(convert(src), encoding="utf-8")
        print(f"{src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")
    # report orphaned targets
    names = {s.name for s in sources}
    for stale in DST_DIR.glob("*.md"):
        if stale.name not in names:
            print(f"Note: {stale.relative_to(ROOT)} has no source any more - delete it if the agent was removed on purpose.")
    print("Done. opencode reads the configuration at start-up only - restart it to pick up changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
