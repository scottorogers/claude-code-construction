#!/usr/bin/env python3
"""
Tests for the issue orchestration graph.

Run: python3 -m unittest discover -s tests -v

Stdlib only, matching the rest of scripts/ — this repo's Python runs wherever
a project engineer's laptop happens to have a Python.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "orchestration")
)

from graph import AccessViolation, Graph, GraphError, Node, SharedState  # noqa: E402
from nodes import (  # noqa: E402
    BudgetNode,
    NetNode,
    NeutralizeNode,
    PrioritizeNode,
    ShrinkNode,
    build_graph,
)


def issue(id_, skill, severity="warning", confidence="medium", description="",
          sheets=(), specs=(), elements=(), rooms=(), grid="", status="open", rfi=None):
    return {
        "id": id_,
        "source_skill": skill,
        "severity": severity,
        "confidence": confidence,
        "status": status,
        "description": description,
        "location": {"sheets": list(sheets), "rooms": list(rooms), "elements": list(elements),
                     "grid": grid, "details": []},
        "document_references": {"spec_sections": list(specs), "drawing_refs": [], "schedule_refs": []},
        "escalated_to_rfi": rfi,
    }


class _Recorder(Node):
    """Reads a key and stashes what it saw, for isolation assertions."""

    def __init__(self, name, reads, writes, seen):
        super().__init__(name, reads, writes)
        self.seen = seen

    def run(self, view):
        for key in sorted(self.reads):
            self.seen[f"{self.name}:{key}"] = view.read(key)
        for key in sorted(self.writes):
            view.write(key, f"from-{self.name}")


class TestAccessControl(unittest.TestCase):
    def test_undeclared_read_raises(self):
        class Sneaky(Node):
            def run(self, view):
                view.read("rfi_log")

        graph = Graph([Sneaky("sneaky", reads=["issues"], writes=["out"])],
                      inputs=["issues", "rfi_log"])
        with self.assertRaises(AccessViolation) as caught:
            graph.run(SharedState({"issues": [], "rfi_log": []}))
        self.assertIn("sneaky", str(caught.exception))

    def test_undeclared_write_raises(self):
        class Sneaky(Node):
            def run(self, view):
                view.write("somewhere_else", 1)

        graph = Graph([Sneaky("sneaky", reads=["issues"], writes=["out"])], inputs=["issues"])
        with self.assertRaises(AccessViolation):
            graph.run(SharedState({"issues": []}))

    def test_node_cannot_read_and_write_same_key(self):
        with self.assertRaises(GraphError):
            Node("bad", reads=["x"], writes=["x"])


class TestGraphStructure(unittest.TestCase):
    def test_missing_producer_is_a_build_error(self):
        with self.assertRaises(GraphError) as caught:
            Graph([_Recorder("a", ["nobody_writes_this"], ["out"], {})], inputs=["issues"])
        self.assertIn("nobody_writes_this", str(caught.exception))

    def test_two_writers_for_one_key_is_a_build_error(self):
        with self.assertRaises(GraphError):
            Graph(
                [_Recorder("a", ["issues"], ["shared"], {}),
                 _Recorder("b", ["issues"], ["shared"], {})],
                inputs=["issues"],
            )

    def test_cycle_is_detected(self):
        with self.assertRaises(GraphError) as caught:
            Graph([_Recorder("a", ["b_out"], ["a_out"], {}),
                   _Recorder("b", ["a_out"], ["b_out"], {})])
        self.assertIn("cycle", str(caught.exception))

    def test_blast_radius_is_exactly_the_downstream_set(self):
        graph = build_graph()
        self.assertEqual(graph.downstream("net"), [])
        self.assertEqual(graph.downstream("prioritize"), ["net"])
        self.assertEqual(
            graph.downstream("shrink"), ["budget", "net", "neutralize", "prioritize"]
        )

    def test_run_order_respects_dependencies(self):
        order = build_graph().order
        self.assertLess(order.index("shrink"), order.index("neutralize"))
        self.assertLess(order.index("neutralize"), order.index("budget"))
        self.assertLess(order.index("budget"), order.index("prioritize"))
        self.assertLess(order.index("prioritize"), order.index("net"))


class TestCycleConsistency(unittest.TestCase):
    def test_late_write_does_not_reach_a_cycle_in_flight(self):
        """The failure this design exists to prevent: two nodes in one cycle
        reading different versions of the same key."""
        seen = {}
        state = SharedState({"capacity": 1, "issues": []})

        class Mutator(Node):
            def run(self, view):
                view.read("issues")
                state.write("capacity", 999)  # a live write mid-cycle
                view.write("stage_one", True)

        class Reader(Node):
            def run(self, view):
                seen["capacity"] = view.read("capacity")
                view.write("stage_two", True)

        graph = Graph(
            [Mutator("mutator", reads=["issues"], writes=["stage_one"]),
             Reader("reader", reads=["capacity", "stage_one"], writes=["stage_two"])],
            inputs=["capacity", "issues"],
        )
        graph.run(state)
        self.assertEqual(seen["capacity"], 1, "reader saw a value written after the freeze")
        self.assertEqual(state.read("capacity"), 999, "the live write should still land")

    def test_an_in_place_edit_mid_cycle_does_not_reach_a_node_already_running(self):
        """A skill appending to the live registry while a cycle runs must not
        change what a later node in that cycle sees."""
        seen = {}
        live_issues = [issue("ISS-1", "pe-review")]
        state = SharedState({"issues": live_issues, "capacity": 1})

        class Mutator(Node):
            def run(self, view):
                live_issues.append(issue("ISS-2", "tag-audit"))  # in place, not via write()
                view.write("stage_one", True)

        class Reader(Node):
            def run(self, view):
                seen["ids"] = [r["id"] for r in view.read("issues")]
                view.write("stage_two", True)

        Graph(
            [Mutator("mutator", reads=["capacity"], writes=["stage_one"]),
             Reader("reader", reads=["issues", "stage_one"], writes=["stage_two"])],
            inputs=["capacity", "issues"],
        ).run(state)
        self.assertEqual(seen["ids"], ["ISS-1"])

    def test_snapshot_is_deep_so_mutating_a_read_cannot_corrupt_state(self):
        state = SharedState({"issues": [{"id": "ISS-1"}]})
        snapshot = state.snapshot()
        snapshot.get("issues")[0]["id"] = "TAMPERED"
        self.assertEqual(state.read("issues")[0]["id"], "ISS-1")

    def test_derived_keys_are_write_once(self):
        class Twice(Node):
            def run(self, view):
                view.write("out", 1)
                view.write("out", 2)

        graph = Graph([Twice("twice", reads=["issues"], writes=["out"])], inputs=["issues"])
        with self.assertRaises(GraphError) as caught:
            graph.run(SharedState({"issues": []}))
        self.assertIn("write-once", str(caught.exception))

    def test_missing_declared_input_is_an_error(self):
        graph = build_graph()
        with self.assertRaises(GraphError):
            graph.run(SharedState({"issues": []}))


def run_nodes(nodes, state_dict, inputs=("issues", "history", "rfi_log", "capacity")):
    return Graph(nodes, inputs=inputs).run(SharedState(state_dict)).derived


class TestShrink(unittest.TestCase):
    def base(self, issues, history=()):
        return run_nodes([ShrinkNode()],
                         {"issues": issues, "history": list(history), "rfi_log": [], "capacity": 5})

    def test_evidence_discounts_a_thinly_cited_issue(self):
        thin = issue("A", "pe-review", "conflict", "high", "no refs")
        cited = issue("B", "pe-review", "conflict", "high", "cited",
                      sheets=["A1.1"], specs=["08 11 13"], elements=["D-1"])
        scored = {r["id"]: r for r in self.base([thin, cited])["scored_issues"]}
        self.assertLess(scored["A"]["score"], scored["B"]["score"])
        self.assertEqual(scored["B"]["score"], 0.75)

    def test_confidence_scales_the_score(self):
        high = issue("A", "s", "conflict", "high", sheets=["A1"], specs=["08"], elements=["D"])
        low = issue("B", "s", "conflict", "low", sheets=["A1"], specs=["08"], elements=["D"])
        scored = {r["id"]: r for r in self.base([high, low])["scored_issues"]}
        self.assertAlmostEqual(scored["B"]["score"] / scored["A"]["score"], 0.35, places=3)

    def test_a_skill_whose_issues_get_dismissed_is_quieted_not_silenced(self):
        history = [issue(f"H{i}", "noisy", status="dismissed") for i in range(30)]
        record = ShrinkNode.track_record(history)
        self.assertLess(record["noisy"], 0.35)
        self.assertGreaterEqual(record["noisy"], 0.25)

    def test_a_short_track_record_is_shrunk_toward_the_prior(self):
        record = ShrinkNode.track_record([issue("H1", "new", status="dismissed")])
        self.assertGreater(record["new"], 0.8, "one dismissal must not condemn a skill")

    def test_unknown_skill_is_not_penalized(self):
        scored = self.base([issue("A", "brand-new", "conflict", "high",
                                  sheets=["A1"], specs=["08"], elements=["D"])])["scored_issues"]
        self.assertEqual(scored[0]["score"], 0.75)


class TestNeutralize(unittest.TestCase):
    def neutralize(self, issues):
        derived = run_nodes(
            [ShrinkNode(), NeutralizeNode()],
            {"issues": issues, "history": [], "rfi_log": [], "capacity": 10},
        )
        return {r["id"]: r for r in derived["residual_issues"]}, derived["root_causes"]

    def test_an_exact_restatement_residualizes_to_nothing(self):
        text = "Door D-142 references HW set 7, not found in 08 71 00"
        a = issue("A", "tag-audit", "warning", "high", text,
                  sheets=["A3.1"], specs=["08 71 00"], elements=["D-142"])
        b = issue("B", "spec-splitter", "warning", "high", text,
                  sheets=["A3.1"], specs=["08 71 00"], elements=["D-142"])
        residual, causes = self.neutralize([a, b])
        follower = min(residual.values(), key=lambda r: r["residual_score"])
        self.assertEqual(follower["residual_score"], 0.0)
        self.assertEqual(len(causes), 1)

    def test_two_questions_about_one_door_are_not_collapsed_into_one(self):
        """Same sheet, same spec section, same door — different questions.
        Location overlap alone must not delete the second one."""
        hardware = issue("A", "tag-audit", "warning", "high",
                         "Door D-142 references hardware set 7 which is not defined",
                         sheets=["A3.1"], specs=["08 71 00"], elements=["D-142"])
        rating = issue("B", "schedule-extractor", "warning", "high",
                       "Door D-142 scheduled as 90 minute rated; plan note says 60 minute",
                       sheets=["A3.1"], specs=["08 71 00"], elements=["D-142"])
        residual, _ = self.neutralize([hardware, rating])
        self.assertGreater(min(r["residual_score"] for r in residual.values()), 0.0)

    def test_unrelated_issues_keep_their_full_score(self):
        a = issue("A", "s", "conflict", "high", "guard height at stair 2 is short",
                  sheets=["A5.2"], specs=["05 52 13"], elements=["G-1"])
        b = issue("B", "s", "conflict", "high", "duct main clashes with ceiling",
                  sheets=["M2.1"], specs=["23 31 13"], rooms=["204"])
        residual, causes = self.neutralize([a, b])
        self.assertEqual(causes, [])
        for record in residual.values():
            self.assertEqual(record["residual_score"], record["score"])


class TestBudgetAndPrioritize(unittest.TestCase):
    def pipeline(self, issues, capacity):
        return run_nodes(
            [ShrinkNode(), NeutralizeNode(), BudgetNode(), PrioritizeNode()],
            {"issues": issues, "history": [], "rfi_log": [], "capacity": capacity},
        )

    def test_a_loud_skill_cannot_take_the_whole_agenda(self):
        loud = [
            issue(f"L{i}", "tag-audit", "warning", "high", f"tag D-{i} missing a callout on A3.1",
                  sheets=[f"A3.{i}"], specs=["08 71 00"], elements=[f"D-{i}"])
            for i in range(20)
        ]
        careful = [
            issue("C1", "pe-review", "conflict", "high", "guard height short at stair 2",
                  sheets=["A5.2"], specs=["05 52 13"], elements=["G-1"]),
            issue("C2", "code-researcher", "conflict", "high", "duct clashes with ceiling in 204",
                  sheets=["M2.1"], specs=["23 31 13"], rooms=["204"]),
        ]
        derived = self.pipeline(loud + careful, capacity=6)
        skills = [r["source_skill"] for r in derived["agenda"]]
        self.assertLessEqual(skills.count("tag-audit"), 4)
        self.assertIn("pe-review", skills)
        self.assertIn("code-researcher", skills)

    def test_capacity_is_never_exceeded(self):
        issues = [
            issue(f"I{i}", f"skill-{i}", "conflict", "high", f"distinct problem number {i} here",
                  sheets=[f"A{i}.1"], specs=[f"0{i} 00 00"], elements=[f"E-{i}"])
            for i in range(9)
        ]
        self.assertEqual(len(self.pipeline(issues, capacity=4)["agenda"]), 4)

    def test_a_safety_issue_is_admitted_even_with_no_budget(self):
        """Nothing in this graph is allowed to hold back a safety finding."""
        crowd = [
            issue(f"W{i}", "tag-audit", "conflict", "high", f"unrelated conflict {i} on its own sheet",
                  sheets=[f"A{i}.1"], specs=[f"0{i} 10 00"], elements=[f"E-{i}"])
            for i in range(8)
        ]
        danger = issue("SAFE", "pe-review", "safety", "low", "exit passage width is under code",
                       sheets=["A1.2"])
        derived = self.pipeline(crowd + [danger], capacity=2)
        admitted = {r["id"]: r for r in derived["agenda"]}
        self.assertIn("SAFE", admitted)
        self.assertEqual(admitted["SAFE"]["admitted_by"], "safety_override")

    def test_no_skill_is_allotted_more_slots_than_it_has_issues(self):
        derived = self.pipeline(
            [issue("A", "solo", "conflict", "high", "one lonely conflict about a beam",
                   sheets=["S1.1"], specs=["05 12 00"], elements=["B-1"])],
            capacity=10,
        )
        self.assertEqual(derived["attention_budget"]["per_skill"], {"solo": 1})

    def test_a_fully_explained_duplicate_is_never_proposed(self):
        text = "Door D-142 references HW set 7, not found in 08 71 00"
        pair = [
            issue("A", "tag-audit", "warning", "high", text,
                  sheets=["A3.1"], specs=["08 71 00"], elements=["D-142"]),
            issue("B", "spec-splitter", "warning", "high", text,
                  sheets=["A3.1"], specs=["08 71 00"], elements=["D-142"]),
        ]
        agenda_ids = {r["id"] for r in self.pipeline(pair, capacity=10)["agenda"]}
        self.assertEqual(len(agenda_ids), 1)


class TestNet(unittest.TestCase):
    def net(self, issues, rfi_log=()):
        return run_nodes(
            [ShrinkNode(), NeutralizeNode(), BudgetNode(), PrioritizeNode(), NetNode()],
            {"issues": issues, "history": [], "rfi_log": list(rfi_log), "capacity": 10},
        )

    def test_a_repeat_of_an_rfi_in_flight_is_not_asked_again(self):
        text = "Hardware set 7 referenced by the door schedule is not defined in 08 71 00"
        derived = self.net(
            [issue("A", "tag-audit", "warning", "high", text,
                   sheets=["A3.1"], specs=["08 71 00"], elements=["D-142"])],
            rfi_log=[{"rfi_number": "RFI-014", "sheets": ["A3.1"], "spec_sections": ["08 71 00"],
                      "description": text, "context": ""}],
        )
        self.assertEqual(derived["net_agenda"], [])
        self.assertEqual(derived["netting_report"]["already_asked"][0]["covered_by"], "RFI-014")

    def test_a_new_question_at_a_known_location_survives_and_is_flagged(self):
        """The dangerous direction: suppressing a live conflict because an
        unrelated RFI happens to cite the same sheet and section."""
        derived = self.net(
            [issue("A", "schedule-extractor", "conflict", "high",
                   "Door D-142 scheduled as 90 minute rated but the plan note says 60 minute",
                   sheets=["A3.1"], specs=["08 71 00"], elements=["D-142"])],
            rfi_log=[{"rfi_number": "RFI-014", "sheets": ["A3.1"], "spec_sections": ["08 71 00"],
                      "description": "Hardware set 7 is not defined in the specification",
                      "context": ""}],
        )
        self.assertEqual(len(derived["net_agenda"]), 1)
        flagged = derived["netting_report"]["possible_duplicates"]
        self.assertEqual([f["id"] for f in flagged], ["A"])

    def test_one_sheet_and_one_division_become_one_question(self):
        pair = [
            issue("A", "pe-review", "warning", "high", "head detail at window W-1 is missing flashing",
                  sheets=["A6.1"], specs=["08 51 13"], elements=["W-1"]),
            issue("B", "spec-splitter", "warning", "high", "sill condition at W-2 lacks an end dam",
                  sheets=["A6.1"], specs=["08 51 13"], elements=["W-2"]),
        ]
        derived = self.net(pair)
        self.assertEqual(len(derived["net_agenda"]), 1)
        self.assertEqual(sorted(derived["net_agenda"][0]["issue_ids"]), ["A", "B"])

    def test_different_sheets_are_not_stapled_into_one_rfi(self):
        pair = [
            issue("A", "pe-review", "warning", "high", "flashing missing at the window head",
                  sheets=["A6.1"], specs=["08 51 13"], elements=["W-1"]),
            issue("B", "pe-review", "warning", "high", "storefront jamb detail is undimensioned",
                  sheets=["A7.4"], specs=["08 43 13"], elements=["SF-2"]),
        ]
        self.assertEqual(len(self.net(pair)["net_agenda"]), 2)

    def test_a_safety_issue_goes_out_on_its_own(self):
        both = [
            issue("SAFE", "pe-review", "safety", "high", "exit passage width is under the code minimum",
                  sheets=["A1.2"], specs=["08 11 13"], rooms=["CORRIDOR 108"]),
            issue("B", "pe-review", "warning", "high", "door 108A undercut is not dimensioned",
                  sheets=["A1.2"], specs=["08 11 13"], elements=["D-108A"]),
        ]
        net_agenda = self.net(both)["net_agenda"]
        safety_row = next(r for r in net_agenda if r["severity"] == "safety")
        self.assertEqual(safety_row["issue_ids"], ["SAFE"])
        self.assertIs(net_agenda[0], safety_row, "safety must lead the agenda")

    def test_one_element_seen_by_two_skills_is_raised_for_reconciliation(self):
        pair = [
            issue("A", "tag-audit", "warning", "high", "beam B-12 is called out as W21x44 on the plan",
                  sheets=["S2.1"], specs=["05 12 00"], elements=["B-12"]),
            issue("B", "schedule-extractor", "warning", "high",
                  "beam B-12 appears in the schedule as W21x50 with a different camber",
                  sheets=["S2.1"], specs=["05 12 00"], elements=["B-12"]),
        ]
        reconcile = self.net(pair)["netting_report"]["reconcile"]
        self.assertEqual([r["element"] for r in reconcile], ["B-12"])
        self.assertEqual(reconcile[0]["source_skills"], ["schedule-extractor", "tag-audit"])


class TestEndToEnd(unittest.TestCase):
    def test_an_empty_registry_produces_an_empty_agenda(self):
        derived = build_graph().run(
            SharedState({"issues": [], "history": [], "rfi_log": [], "capacity": 5})
        ).derived
        self.assertEqual(derived["net_agenda"], [])
        self.assertEqual(derived["netting_report"]["questions_saved"], 0)

    def test_every_declared_output_is_produced(self):
        context = build_graph().run(
            SharedState({
                "issues": [issue("A", "pe-review", "conflict", "high", "guard height is short",
                                 sheets=["A5.2"], specs=["05 52 13"], elements=["G-1"])],
                "history": [], "rfi_log": [], "capacity": 5,
            })
        )
        for key in ("scored_issues", "residual_issues", "root_causes", "attention_budget",
                    "agenda", "net_agenda", "netting_report"):
            self.assertIn(key, context.derived)


if __name__ == "__main__":
    unittest.main()
