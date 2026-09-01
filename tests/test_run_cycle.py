#!/usr/bin/env python3
"""
Tests for run_cycle.py — the CLI that feeds the orchestration graph.

The graph's own tests take their inputs as given. These cover the layer that
builds those inputs from `.construction/issues/`, where a silent omission does
real damage: if the RFI log were built without its subject text, netting would
fall back to matching on location alone and start suppressing new questions
that happen to cite a sheet already under an open RFI.

Run: python3 -m unittest discover -s tests
"""

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts" / "orchestration"))

import run_cycle  # noqa: E402


def issue_record(id_, skill="pe-review", severity="conflict", confidence="high",
                 description="guard height is short at stair 2", sheets=("A5.2",),
                 specs=("05 52 13",), status="open", rfi=None, subject=""):
    return {
        "id": id_,
        "source_skill": skill,
        "severity": severity,
        "confidence": confidence,
        "status": status,
        "description": description,
        "potential_rfi_subject": subject,
        "location": {"sheets": list(sheets), "rooms": [], "elements": [], "grid": "", "details": []},
        "document_references": {"spec_sections": list(specs), "drawing_refs": [], "schedule_refs": []},
        "escalated_to_rfi": rfi,
    }


class RegistryFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.issues_dir = Path(self.tmp) / "issues"
        self.issues_dir.mkdir()
        self.addCleanup(shutil.rmtree, self.tmp)

    def write(self, record):
        (self.issues_dir / f"{record['id']}.json").write_text(json.dumps(record))
        return record


class TestLoadRegistry(RegistryFixture):
    def test_reads_every_issue_record(self):
        self.write(issue_record("ISS-2026-0001"))
        self.write(issue_record("ISS-2026-0002"))
        self.assertEqual(len(run_cycle.load_registry(self.issues_dir)), 2)

    def test_a_corrupt_record_is_skipped_not_fatal(self):
        """One unparseable file must not take the whole cycle down with it."""
        self.write(issue_record("ISS-2026-0001"))
        (self.issues_dir / "ISS-2026-0002.json").write_text("{ this is not json")
        captured = io.StringIO()
        with redirect_stderr(captured):
            records = run_cycle.load_registry(self.issues_dir)
        self.assertEqual([r["id"] for r in records], ["ISS-2026-0001"])
        self.assertIn("ISS-2026-0002.json", captured.getvalue())

    def test_a_missing_directory_is_an_empty_registry(self):
        self.assertEqual(run_cycle.load_registry(Path(self.tmp) / "nope"), [])


class TestBuildRfiLog(RegistryFixture):
    def test_only_escalated_issues_enter_the_log(self):
        history = [
            issue_record("ISS-1", status="escalated", rfi="RFI-014"),
            issue_record("ISS-2", status="open"),
            issue_record("ISS-3", status="dismissed"),
        ]
        log = run_cycle.build_rfi_log(history)
        self.assertEqual([e["rfi_number"] for e in log], ["RFI-014"])

    def test_the_log_carries_the_subject_text_netting_matches_on(self):
        """Load-bearing: without description, NetNode._already_asked has no
        subject to compare and degrades to suppressing on location alone."""
        text = "Hardware set 7 is not defined in section 08 71 00"
        log = run_cycle.build_rfi_log(
            [issue_record("ISS-1", status="escalated", rfi="RFI-014", description=text,
                          subject="Undefined hardware set")]
        )
        self.assertEqual(log[0]["description"], text)
        self.assertEqual(log[0]["context"], "Undefined hardware set")

    def test_the_log_carries_the_location_netting_matches_on(self):
        log = run_cycle.build_rfi_log(
            [issue_record("ISS-1", status="escalated", rfi="RFI-014",
                          sheets=["A3.1"], specs=["08 71 00"])]
        )
        self.assertEqual(log[0]["sheets"], ["A3.1"])
        self.assertEqual(log[0]["spec_sections"], ["08 71 00"])


class TestBuildState(RegistryFixture):
    def test_only_live_issues_are_offered_to_the_graph(self):
        for status in ("open", "reviewed", "resolved", "dismissed", "escalated"):
            self.write(issue_record(f"ISS-{status}", status=status))
        state = run_cycle.build_state(self.issues_dir, capacity=5)
        self.assertEqual(
            sorted(r["id"] for r in state.read("issues")), ["ISS-open", "ISS-reviewed"]
        )

    def test_history_keeps_closed_issues_so_track_record_can_be_scored(self):
        self.write(issue_record("ISS-1", status="dismissed"))
        self.write(issue_record("ISS-2", status="open"))
        state = run_cycle.build_state(self.issues_dir, capacity=5)
        self.assertEqual(len(state.read("history")), 2)
        self.assertEqual(len(state.read("issues")), 1)


class TestRenderReport(RegistryFixture):
    def result_for(self, records):
        from nodes import build_graph

        for record in records:
            self.write(record)
        state = run_cycle.build_state(self.issues_dir, capacity=10)
        context = build_graph().run(state)
        result = dict(context.derived)
        result["cycle_version"] = context.snapshot.version
        return result

    def test_an_empty_cycle_says_so_rather_than_rendering_an_empty_table(self):
        report = run_cycle.render_report(self.result_for([]), "CYC-TEST")
        self.assertIn("Nothing to escalate this cycle", report)

    def test_the_report_names_the_issues_on_the_agenda(self):
        report = run_cycle.render_report(self.result_for([issue_record("ISS-2026-0001")]), "CYC-TEST")
        self.assertIn("CYC-TEST", report)
        self.assertIn("ISS-2026-0001", report)
        self.assertIn("Attention budget", report)

    def test_a_suppressed_duplicate_is_reported_with_the_rfi_covering_it(self):
        text = "Hardware set 7 referenced by the door schedule is not defined in 08 71 00"
        report = run_cycle.render_report(
            self.result_for([
                issue_record("ISS-2026-0001", status="escalated", rfi="RFI-014",
                             description=text, sheets=["A3.1"], specs=["08 71 00"]),
                issue_record("ISS-2026-0002", skill="tag-audit-and-takeoff", description=text,
                             sheets=["A3.1"], specs=["08 71 00"]),
            ]),
            "CYC-TEST",
        )
        self.assertIn("Already asked", report)
        self.assertIn("RFI-014", report)


class TestCommandLine(RegistryFixture):
    def run_cli(self, *args):
        completed = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "orchestration" / "run_cycle.py"), *args],
            capture_output=True, text=True, cwd=self.tmp,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return completed

    def test_describe_prints_the_graph(self):
        stdout = self.run_cli("describe").stdout
        for node in ("shrink", "neutralize", "budget", "prioritize", "net"):
            self.assertIn(node, stdout)

    def test_blast_radius_is_reported_for_a_named_node(self):
        payload = json.loads(self.run_cli("blast-radius", "--node", "prioritize").stdout)
        self.assertEqual(payload["downstream"], ["net"])

    def test_a_run_writes_a_cycle_directory(self):
        self.write(issue_record("ISS-2026-0001"))
        cycles = Path(self.tmp) / "cycles"
        self.run_cli("--issues-dir", str(self.issues_dir), "--cycles-dir", str(cycles),
                     "run", "--capacity", "5")
        written = sorted(p.name for p in cycles.glob("CYC-*/*"))
        self.assertEqual(written, ["report.md", "result.json"])

    def test_a_dry_run_writes_nothing(self):
        self.write(issue_record("ISS-2026-0001"))
        cycles = Path(self.tmp) / "cycles"
        self.run_cli("--issues-dir", str(self.issues_dir), "--cycles-dir", str(cycles),
                     "run", "--dry-run")
        self.assertFalse(cycles.exists())

    def test_a_run_never_overwrites_a_prior_cycle_in_the_same_directory(self):
        """safe_output_path is the repo's non-destructive merge rule; a second
        cycle landing in the same directory must version rather than clobber."""
        self.write(issue_record("ISS-2026-0001"))
        cycles = Path(self.tmp) / "cycles"
        target = cycles / "CYC-FIXED"
        target.mkdir(parents=True)
        (target / "result.json").write_text('{"prior": true}')

        state = run_cycle.build_state(self.issues_dir, capacity=5)
        from nodes import build_graph
        from shared import safe_output_path

        result = dict(build_graph().run(state).derived)
        with open(safe_output_path(str(target / "result.json")), "w") as handle:
            json.dump(result, handle)

        self.assertEqual(json.loads((target / "result.json").read_text()), {"prior": True})
        self.assertTrue((target / "result_v2.json").exists())

    def test_the_run_output_is_parseable_json_by_default(self):
        self.write(issue_record("ISS-2026-0001"))
        payload = json.loads(
            self.run_cli("--issues-dir", str(self.issues_dir), "run", "--dry-run").stdout
        )
        self.assertIn("net_agenda", payload)
        self.assertTrue(payload["cycle_id"].startswith("CYC-"))


if __name__ == "__main__":
    unittest.main()
