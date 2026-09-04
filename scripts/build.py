#!/usr/bin/env python3
"""build.py - build (or check) a harness in a target project from this skill's templates.

The harness is never copied by hand: this script carries every file under assets/project/
into the target project, generates CLAUDE.md (one line: @AGENTS.md), and reports what it
did. It is idempotent - an existing file is never overwritten unless --force names it - so
it can be run again after the skill was updated (git pull in the skill folder) to see what
the project is missing or what has drifted.

    python3 scripts/build.py <target>            build: copy what is missing, report the rest
    python3 scripts/build.py <target> --check    compare only, change nothing (exit 1 on drift)
    python3 scripts/build.py <target> --force a b  overwrite the named files (paths relative
                                                   to the target, e.g. tools/agent-start.py)

Exit codes: 0 done / nothing to do, 1 drift found (--check) or a file could not be written,
2 wrong usage. Reads nothing outside the skill and the target; needs no network.
"""

import argparse
import filecmp
import pathlib
import shutil
import sys

SKILL_ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "project"
GENERATED = {"CLAUDE.md": "@AGENTS.md\n"}   # not stored as a template: a CLAUDE.md inside the
                                             # skill would be loaded as a rule file while the
                                             # skill itself is edited


def skill_version() -> str:
    """Read metadata.version from SKILL.md without a YAML library (the frontmatter is flat)."""
    text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("version:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return "unknown"


def template_files() -> list[pathlib.Path]:
    files = [p for p in TEMPLATE_ROOT.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    return sorted(p.relative_to(TEMPLATE_ROOT) for p in files)


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.split("\n\n")[0])
    ap.add_argument("target", nargs="?", help="project folder that gets the harness")
    ap.add_argument("--check", action="store_true", help="compare only, write nothing")
    ap.add_argument("--force", nargs="*", default=[], metavar="FILE",
                    help="overwrite these target-relative files with the skill's version")
    args = ap.parse_args()
    if not args.target:
        print(__doc__.strip())
        return 2

    target = pathlib.Path(args.target).expanduser().resolve()
    if not target.is_dir():
        print(f"Target is not a directory: {target}\n"
              f"Create the project folder first (mkdir, git init), then run the build again.")
        return 2
    if target == SKILL_ROOT or SKILL_ROOT in target.parents:
        print(f"Refusing: {target} is the skill itself. The harness is built into a PROJECT "
              f"folder - pass that folder as the argument.")
        return 2
    if not (TEMPLATE_ROOT / "AGENTS.md").is_file():
        print(f"Templates missing under {TEMPLATE_ROOT} - the skill checkout is incomplete; "
              f"re-clone it.")
        return 2

    created: list[str] = []
    same: list[str] = []
    differs: list[str] = []
    overwritten: list[str] = []
    failed: list[str] = []
    force = {pathlib.PurePosixPath(f).as_posix() for f in args.force}

    def place(rel: str, src: pathlib.Path | None, content: str | None) -> None:
        dst = target / rel
        exists = dst.exists()
        if exists:
            if src is not None:
                equal = filecmp.cmp(src, dst, shallow=False)
            else:
                equal = dst.read_text(encoding="utf-8", errors="replace") == content
            if equal:
                same.append(rel)
                return
            if rel not in force:
                differs.append(rel)
                return
        if args.check:
            (differs if exists else created).append(rel)
            return
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if src is not None:
                shutil.copy2(src, dst)
            else:
                dst.write_text(content, encoding="utf-8")
        except OSError as exc:
            failed.append(f"{rel}: {exc}")
            return
        (overwritten if exists else created).append(rel)

    for rel in template_files():
        place(rel.as_posix(), TEMPLATE_ROOT / rel, None)
    for rel, content in GENERATED.items():
        place(rel, None, content)

    unknown = sorted(force - set(created) - set(overwritten) - set(same) - set(differs))
    mode = "check" if args.check else "build"
    print(f"harness {mode}: skill v{skill_version()} -> {target}")
    for label, items in (("created" if not args.check else "missing", created),
                         ("overwritten", overwritten),
                         ("differs from the skill (kept)", differs)):
        if items:
            print(f"\n{label} ({len(items)}):")
            for item in items:
                print(f"  {item}")
    if same:
        print(f"\nunchanged: {len(same)} file(s) identical to the skill")
    if unknown:
        print(f"\n--force named files that are not templates: {', '.join(unknown)}")
    if failed:
        print("\ncould not write:")
        for item in failed:
            print(f"  {item}")

    print()
    if args.check:
        if created or differs:
            print("Next: for each file that differs, HARNESS.md of the project says whether the "
                  "difference is a recorded deviation (keep it) or drift (take the skill's "
                  "version: --force <file>). Missing files: run the build without --check.")
            return 1
        print("The project matches the skill's templates.")
        return 0
    if created:
        print("Next: python3 tools/sync-agents.py in the project (generates the other agents' "
              "subagent formats), then the guided setup in references/setup.md.")
    if differs:
        print("Files that differ were kept. Decide with HARNESS.md whether each is a deviation "
              "or drift; --force <file> takes the skill's version.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
