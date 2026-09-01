#!/usr/bin/env python3
"""
run_cycle.py — Run one orchestration cycle over the issue registry.

Reads `.construction/issues/`, freezes it, runs the graph, and writes the
netted review agenda to `.construction/cycles/<cycle_id>/`. Nothing is
escalated here and no issue record is modified — the agenda says what is worth
a person's attention this cycle and why, and rfi-drafter takes it from there.

Usage:
  run_cycle.py run [--capacity 10] [--issues-dir DIR] [--report] [--dry-run]
  run_cycle.py describe                  # nodes, edges, run order, blast radius
  run_cycle.py blast-radius --node NAME  # what a bad node can reach
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from graph import SharedState  # noqa: E402
from nodes import build_graph  # noqa: E402
from shared import safe_output_path  # noqa: E402

DEFAULT_ISSUES_DIR = ".construction/issues"
DEFAULT_CYCLES_DIR = ".construction/cycles"
LIVE_STATUSES = ("open", "reviewed")


def load_registry(issues_dir):
    """Every issue record on disk, newest last."""
    directory = Path(issues_dir)
    if not directory.is_dir():
        return []
    records = []
    for path in sorted(directory.glob("ISS-*.json")):
        try:
            with open(path) as handle:
                records.append(json.load(handle))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"WARN: skipping unreadable issue {path.name}: {exc}", file=sys.stderr)
    return records


def build_rfi_log(history):
    """The questions already in flight, so the graph does not ask them twice."""
    log = []
    for record in history:
        rfi_number = record.get("escalated_to_rfi")
        if not rfi_number:
            continue
        log.append(
            {
                "rfi_number": rfi_number,
                "from_issue": record.get("id"),
                "sheets": (record.get("location") or {}).get("sheets") or [],
                "spec_sections": (record.get("document_references") or {}).get("spec_sections") or [],
                # The subject text matters: netting must tell a new question at a
                # known location from a repeat of one already asked.
                "description": record.get("description", ""),
                "context": record.get("potential_rfi_subject", ""),
            }
        )
    return log


def build_state(issues_dir, capacity):
    history = load_registry(issues_dir)
    live = [r for r in history if r.get("status") in LIVE_STATUSES]
    return SharedState(
        {
            "issues": live,
            "history": history,
            "rfi_log": build_rfi_log(history),
            "capacity": capacity,
        }
    )


def render_report(result, cycle_id):
    budget = result["attention_budget"]
    netting = result["netting_report"]
    lines = [
        f"# Review cycle {cycle_id}",
        "",
        f"- State version at freeze: {result['cycle_version']}",
        f"- Issues in queue: {len(result['scored_issues'])}",
        f"- After neutralization: {sum(1 for r in result['residual_issues'] if r['residual_score'] > 0)}"
        f" live, {len(result['root_causes'])} shared root cause(s)",
        f"- Review capacity: {budget['capacity']}",
        f"- Agenda: {len(result['agenda'])} issues → {netting['net_questions']} question(s)"
        f" ({netting['questions_saved']} saved by netting)",
        "",
    ]

    if result["root_causes"]:
        lines += ["## Root causes absorbing duplicate findings", ""]
        for cause in result["root_causes"]:
            factors = ", ".join(cause["shared_factors"]) or "(location overlap)"
            lines.append(
                f"- **{cause['head']}** explains {', '.join(cause['explains'])} — shared: {factors}"
            )
        lines.append("")

    if budget["per_skill"]:
        lines += [
            f"## Attention budget ({budget['basis']})",
            "",
            "| Skill | Slots |",
            "|---|---|",
        ]
        for skill, slots in sorted(budget["per_skill"].items(), key=lambda kv: (-kv[1], kv[0])):
            lines.append(f"| {skill} | {slots} |")
        lines.append("")

    lines += ["## Netted agenda", ""]
    if not result["net_agenda"]:
        lines.append("_Nothing to escalate this cycle._")
    else:
        lines += ["| # | Group | Sev | Score | Issues | Sheets | Sources |", "|---|---|---|---|---|---|---|"]
        for index, item in enumerate(result["net_agenda"], 1):
            lines.append(
                f"| {index} | {item['division_name']} | {item['severity']} | {item['score']} | "
                f"{', '.join(item['issue_ids'])} | {', '.join(item['sheets']) or '—'} | "
                f"{', '.join(item['source_skills'])} |"
            )
    lines.append("")

    if netting["already_asked"]:
        lines += ["## Already asked — not re-sending", ""]
        for entry in netting["already_asked"]:
            lines.append(
                f"- {entry['id']} is covered by {entry['covered_by']} "
                f"(subject overlap {entry['subject_overlap']})"
            )
        lines.append("")

    if netting["possible_duplicates"]:
        lines += ["## Same location as an RFI in flight — kept, verify before sending", ""]
        for entry in netting["possible_duplicates"]:
            lines.append(f"- {entry['id']} sits near {entry['near']} — {entry['note']}")
        lines.append("")

    if netting["reconcile"]:
        lines += ["## Reconcile before sending", ""]
        for entry in netting["reconcile"]:
            lines.append(
                f"- **{entry['element']}**: {', '.join(entry['issue_ids'])} "
                f"from {', '.join(entry['source_skills'])} — {entry['note']}"
            )
        lines.append("")

    return "\n".join(lines)


def cmd_run(args):
    graph = build_graph()
    state = build_state(args.issues_dir, args.capacity)
    context = graph.run(state)

    result = dict(context.derived)
    result["cycle_version"] = context.snapshot.version
    cycle_id = "CYC-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

    if not args.dry_run:
        cycle_dir = Path(args.cycles_dir) / cycle_id
        cycle_dir.mkdir(parents=True, exist_ok=True)
        with open(safe_output_path(str(cycle_dir / "result.json")), "w") as handle:
            json.dump(result, handle, indent=2)
        with open(safe_output_path(str(cycle_dir / "report.md")), "w") as handle:
            handle.write(render_report(result, cycle_id))
        print(f"OK: cycle written → {cycle_dir}", file=sys.stderr)

    if args.report:
        print(render_report(result, cycle_id))
    else:
        print(json.dumps({"cycle_id": cycle_id, **result}, indent=2))


def cmd_describe(args):
    print(build_graph().describe())


def cmd_blast_radius(args):
    graph = build_graph()
    print(json.dumps({"node": args.node, "downstream": graph.downstream(args.node)}, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Run the issue orchestration graph")
    parser.add_argument("--issues-dir", default=DEFAULT_ISSUES_DIR)
    parser.add_argument("--cycles-dir", default=DEFAULT_CYCLES_DIR)
    sub = parser.add_subparsers(dest="command", required=True)

    run_p = sub.add_parser("run", help="Run one cycle and write the agenda")
    run_p.add_argument("--capacity", type=int, default=10, help="Issues a reviewer can work this cycle")
    run_p.add_argument("--report", action="store_true", help="Print markdown instead of JSON")
    run_p.add_argument("--dry-run", action="store_true", help="Do not write the cycle directory")
    run_p.set_defaults(func=cmd_run)

    sub.add_parser("describe", help="Print the graph").set_defaults(func=cmd_describe)

    blast_p = sub.add_parser("blast-radius", help="Nodes a given node can affect")
    blast_p.add_argument("--node", required=True)
    blast_p.set_defaults(func=cmd_blast_radius)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
