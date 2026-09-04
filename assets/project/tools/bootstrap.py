#!/usr/bin/env python3
"""bootstrap.py - make a fresh checkout of this project workable.

Some agent configuration lives OUTSIDE the repository and therefore does not survive a
`git clone`. hermes, for example, loads project skills only for trusted projects and keeps
that trust list in ~/.hermes/config.yaml. Until it is re-established, the building block
simply does not take hold - with no error, which is the dangerous part.

A README line does not fix this: nobody reads a README twice. So the step goes here, in a
script that is idempotent, safe to run repeatedly, and silent when there is nothing to do -
and the script is wired to run automatically (a SessionStart hook for agents that have hooks;
a line in AGENTS.md for the rest).

Add your project's own one-time local setup as a further step_* function and call it in
main(). Keep the rule: fix what is local and reversible, only REPORT anything that needs a
human, a secret, or a network call.
"""

import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

did: list[str] = []      # changed something
todo: list[str] = []     # needs a human before work can proceed
fine: list[str] = []     # already in order


def run(cmd: list[str], cwd: pathlib.Path = ROOT) -> tuple[int, str]:
    """Never raises: a missing binary comes back as an exit code, so the caller reports a
    finding instead of dying with a traceback."""
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=120)
    except FileNotFoundError:
        return 127, f"{cmd[0]}: not installed or not on PATH"
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 126, f"{cmd[0]}: {exc}"
    return p.returncode, p.stdout + p.stderr


def step_hermes() -> None:
    """hermes reads project skills only for trusted projects, and the trust list is
    machine-local. Skip silently if hermes is not installed or the project has no skills
    where hermes looks."""
    if shutil.which("hermes") is None:
        return
    if not ((ROOT / ".hermes" / "skills").exists() or (ROOT / ".agents" / "skills").exists()):
        return
    code, out = run(["hermes", "skills", "trust", str(ROOT)])
    if code != 0:
        todo.append(f"`hermes skills trust {ROOT}` failed: {out.strip()[:200]}")
    elif "Already trusted" in out:
        fine.append("hermes trusts this project's skills.")
    else:
        did.append("Trusted this project for hermes, so it loads the project skills. "
                   "Note it takes effect from the NEXT hermes session - it reads its skill "
                   "configuration at start-up.")


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Make a fresh checkout workable. Without arguments: run the local setup "
                    "and report whatever needs a human.")
    ap.add_argument("--quiet", action="store_true",
                    help="print nothing when everything is already in order (used by the hook)")
    args = ap.parse_args()

    step_hermes()

    # Quiet mode is the session-start hook: it speaks only when something changed or is
    # actually blocking. Anything that merely *would* be needed later belongs in the tool
    # that needs it, not in a message on every session start.
    if args.quiet and not did and not todo:
        return 0

    print("# bootstrap.py\n")
    for d in did:
        print(f"- DONE: {d}")
    if not args.quiet:
        for f in fine:
            print(f"- OK: {f}")
    for t in todo:
        print(f"- TODO: {t}")
    if not did and not todo and not args.quiet:
        print("Nothing to do.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
