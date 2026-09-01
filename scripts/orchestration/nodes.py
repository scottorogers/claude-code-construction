#!/usr/bin/env python3
"""
nodes.py — The five nodes of the issue orchestration graph.

Each skill writes issues into `.construction/issues/` without knowing what the
other skills found. Left alone, that queue double-counts one root cause as five
findings, lets a chatty skill crowd out a careful one, and sends the architect
two RFIs asking the same question. These nodes sit between detection and
escalation and fix each of those, in this order:

  shrink      discount each issue by how much the record actually supports it
  neutralize  strip the part of an issue already explained by a shared cause
  budget      split review attention by dispersion, not by issue count
  prioritize  select under the constraints, rather than select then trim
  net         merge what would become one question; drop what was already asked

Ordering matters as much as the steps. Neutralization runs before budgeting so
a skill is not rewarded for reporting one root cause five times, and the
constraints live inside selection so an item that could never be worked is
never proposed.
"""

import os
import re
from collections import defaultdict

from graph import Graph, Node

SEVERITY_WEIGHT = {"safety": 1.0, "conflict": 0.75, "warning": 0.40, "info": 0.15}
SEVERITY_RANK = {"safety": 0, "conflict": 1, "warning": 2, "info": 3}
CONFIDENCE_WEIGHT = {"high": 1.0, "medium": 0.65, "low": 0.35}

MIN_EVIDENCE_REFS = 3      # document references at which evidence stops discounting
TRACK_RECORD_PRIOR = 5     # issues before a skill's dismissal rate is fully credible
TRACK_RECORD_FLOOR = 0.25  # a noisy skill is quieted, never silenced
SIMILARITY_THRESHOLD = 0.5 # overlap at which two issues are treated as one root cause
FACTOR_WEIGHT = 0.6        # share of similarity from where the issue is
SUBJECT_WEIGHT = 0.4       # share of similarity from what the issue is about
SAME_QUESTION_THRESHOLD = 0.25  # subject overlap at which an issue repeats an RFI in flight

GRAPH_INPUTS = ("issues", "history", "rfi_log", "capacity")


def _factor_tokens(issue):
    """The 'exposures' an issue carries: where it is and what it is about.

    Two issues sharing most of these are usually one problem written twice.
    """
    location = issue.get("location") or {}
    refs = issue.get("document_references") or {}
    tokens = set()
    for sheet in location.get("sheets") or []:
        tokens.add(f"sheet:{sheet}")
    for section in refs.get("spec_sections") or []:
        tokens.add(f"spec:{section}")
    for room in location.get("rooms") or []:
        tokens.add(f"room:{room}")
    for element in location.get("elements") or []:
        tokens.add(f"elem:{element}")
    if location.get("grid"):
        tokens.add(f"grid:{location['grid']}")
    return tokens


def _evidence_count(issue):
    location = issue.get("location") or {}
    refs = issue.get("document_references") or {}
    count = sum(
        len(seq or [])
        for seq in (
            location.get("sheets"),
            location.get("rooms"),
            location.get("elements"),
            refs.get("spec_sections"),
            refs.get("schedule_refs"),
        )
    )
    return count + (1 if location.get("grid") else 0)


STOPWORDS = {
    "and", "are", "but", "for", "from", "has", "have", "not", "the", "that", "this", "with",
    "was", "were", "per", "its", "into", "than", "then", "there", "these", "does", "shown",
    "should", "would", "could", "must", "may", "any", "all", "one", "two",
}


def _subject_terms(issue):
    """What the issue is about, as bare terms. Two findings at one location are
    not one finding — a door's hardware set and its fire rating are different
    questions about the same door — so location overlap alone must not collapse
    them."""
    text = f"{issue.get('description', '')} {issue.get('context', '')}".lower()
    return {t for t in re.findall(r"[a-z0-9][a-z0-9\-]{2,}", text) if t not in STOPWORDS}


def _similarity(factors_a, terms_a, factors_b, terms_b):
    """Weighted overlap of where two issues are and what they are about."""
    return round(
        FACTOR_WEIGHT * _jaccard(factors_a, factors_b)
        + SUBJECT_WEIGHT * _jaccard(terms_a, terms_b),
        4,
    )


def _jaccard(left, right):
    if not left or not right:
        return 0.0
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def _apportion(weights, total):
    """Largest-remainder apportionment, so the parts sum to the whole exactly."""
    if total <= 0 or not weights:
        return {k: 0 for k in weights}
    scale = sum(weights.values())
    if scale <= 0:
        return {k: 0 for k in weights}
    exact = {k: total * w / scale for k, w in weights.items()}
    floors = {k: int(v) for k, v in exact.items()}
    remainder = total - sum(floors.values())
    ranked = sorted(exact, key=lambda k: (-(exact[k] - floors[k]), k))
    for key in ranked[:remainder]:
        floors[key] += 1
    return floors


class ShrinkNode(Node):
    """Discount each issue by how much the record actually supports it.

    A raw severity is the equivalent of a bare buy/sell: it gives the nodes
    downstream nothing to weigh. Three things scale it down here — the
    reporting skill's own stated confidence, how many documents the issue
    actually cites, and how often that skill's past issues were dismissed.
    The dismissal rate is itself shrunk toward the prior, so a skill is not
    condemned on its first two findings.
    """

    def __init__(self):
        super().__init__("shrink", reads=["issues", "history"], writes=["scored_issues"])

    @staticmethod
    def track_record(history):
        outcomes = defaultdict(lambda: [0, 0])  # skill -> [closed, dismissed]
        for record in history:
            status = record.get("status")
            if status not in ("resolved", "dismissed", "escalated"):
                continue
            stats = outcomes[record.get("source_skill", "unknown")]
            stats[0] += 1
            if status == "dismissed":
                stats[1] += 1
        scores = {}
        for skill, (closed, dismissed) in outcomes.items():
            credibility = closed / (closed + TRACK_RECORD_PRIOR)
            rate = dismissed / closed if closed else 0.0
            scores[skill] = max(TRACK_RECORD_FLOOR, 1.0 - credibility * rate)
        return scores

    def run(self, view):
        issues = view.read("issues", []) or []
        record = self.track_record(view.read("history", []) or [])

        scored = []
        for issue in issues:
            severity = issue.get("severity", "info")
            skill = issue.get("source_skill", "unknown")
            evidence = _evidence_count(issue)

            confidence_w = CONFIDENCE_WEIGHT.get(issue.get("confidence", "medium"), 0.35)
            evidence_w = min(1.0, evidence / MIN_EVIDENCE_REFS) if MIN_EVIDENCE_REFS else 1.0
            record_w = record.get(skill, 1.0)
            reliability = confidence_w * evidence_w * record_w

            scored.append(
                dict(
                    issue,
                    severity_weight=SEVERITY_WEIGHT.get(severity, 0.15),
                    evidence_refs=evidence,
                    reliability=round(reliability, 4),
                    score=round(SEVERITY_WEIGHT.get(severity, 0.15) * reliability, 4),
                    factors=sorted(_factor_tokens(issue)),
                )
            )
        scored.sort(key=lambda r: -r["score"])
        view.write("scored_issues", scored)


class NeutralizeNode(Node):
    """Strip the part of each issue already explained by a shared root cause.

    Two issues can read as unrelated and still be one problem — a missing
    hardware set cited from the door schedule and again from the spec is one
    question, not two. Issues are clustered on the location and reference
    tokens they share; the best-supported member keeps its full score and the
    rest pass on only the residual, the part the shared cause does not explain.
    An exact locational duplicate residualizes to zero and never reaches the
    agenda.
    """

    def __init__(self):
        super().__init__(
            "neutralize", reads=["scored_issues"], writes=["residual_issues", "root_causes"]
        )

    def run(self, view):
        scored = view.read("scored_issues", []) or []
        heads = []  # (head_issue, factor_set, term_set, [(member, similarity)])

        for issue in sorted(scored, key=lambda r: (-r["score"], r.get("id", ""))):
            factors = set(issue.get("factors") or [])
            terms = _subject_terms(issue)
            match = best = None
            for entry in heads:
                similarity = _similarity(factors, terms, entry[1], entry[2])
                if similarity >= SIMILARITY_THRESHOLD and (best is None or similarity > best):
                    match, best = entry, similarity
            if match is None:
                heads.append((issue, factors, terms, []))
            else:
                match[3].append((issue, best))

        residual = []
        root_causes = []
        for head, head_factors, _head_terms, members in heads:
            residual.append(
                dict(
                    head,
                    residual_score=head["score"],
                    explained_fraction=0.0,
                    explained_by=[],
                    cluster_head=head.get("id"),
                )
            )
            for member, similarity in members:
                residual.append(
                    dict(
                        member,
                        residual_score=round(member["score"] * (1.0 - similarity), 4),
                        explained_fraction=similarity,
                        explained_by=sorted(set(member.get("factors") or []) & head_factors),
                        cluster_head=head.get("id"),
                    )
                )
            if members:
                root_causes.append(
                    {
                        "head": head.get("id"),
                        "shared_factors": sorted(
                            set.intersection(
                                head_factors, *[set(m.get("factors") or []) for m, _ in members]
                            )
                        ),
                        "explains": [m.get("id") for m, _ in members],
                        "gross_score": round(head["score"] + sum(m["score"] for m, _ in members), 4),
                        "net_score": round(
                            head["score"]
                            + sum(round(m["score"] * (1.0 - sim), 4) for m, sim in members),
                            4,
                        ),
                    }
                )

        residual.sort(key=lambda r: -r["residual_score"])
        view.write("residual_issues", residual)
        view.write("root_causes", root_causes)


class BudgetNode(Node):
    """Cap how much of one review cycle any single skill can take.

    Ranking every issue and taking the top N lets one skill own the whole
    agenda. A skill that emits fifty near-identical tag warnings is not fifty
    times more informative than the one that found three code conflicts, but a
    pure ranking treats volume as if it were conviction. Each contributing
    skill gets an equal share of capacity, floored at one slot so nothing is
    silenced outright; capacity that a skill cannot fill is released, and the
    prioritize node spends it on the best of whatever is left.

    Deliberately NOT weighted by score dispersion. Reliability is already
    priced into the score upstream, and charging for it twice would penalize
    exactly the skill whose findings range from routine to safety-critical.
    The honest weighting here would be reviewer minutes per issue — an hour to
    adjudicate a code conflict against thirty seconds for a missing tag — which
    equal slots hands out just as unevenly as equal dollars hand out risk. That
    needs measured handling times this repo does not yet collect, so this node
    caps concentration and says so rather than inventing the numbers.
    """

    def __init__(self):
        super().__init__("budget", reads=["residual_issues", "capacity"], writes=["attention_budget"])

    def run(self, view):
        residual = view.read("residual_issues", []) or []
        capacity = int(view.read("capacity", 0) or 0)

        by_skill = defaultdict(list)
        for issue in residual:
            if issue["residual_score"] > 0:
                by_skill[issue.get("source_skill", "unknown")].append(issue["residual_score"])

        if not by_skill:
            view.write(
                "attention_budget",
                {"capacity": capacity, "per_skill": {}, "basis": "equal-share concentration cap"},
            )
            return

        available = {skill: len(scores) for skill, scores in by_skill.items()}
        target = min(capacity, sum(available.values()))
        allotted = _apportion({skill: 1.0 for skill in by_skill}, target)

        # Guarantee every contributing skill a voice, then trim the largest
        # allocations to pay for it — a floor is worth more than exact parity.
        for skill in allotted:
            if allotted[skill] == 0 and available[skill] > 0 and sum(allotted.values()) < target:
                allotted[skill] = 1
        while sum(allotted.values()) > target:
            richest = max(allotted, key=lambda s: (allotted[s], s))
            if allotted[richest] <= 1:
                break
            allotted[richest] -= 1

        # No skill can hold more slots than it has issues; release the surplus.
        for skill in allotted:
            allotted[skill] = min(allotted[skill], available[skill])

        view.write(
            "attention_budget",
            {
                "capacity": capacity,
                "per_skill": allotted,
                "released": max(0, target - sum(allotted.values())),
                "basis": "equal-share concentration cap",
            },
        )


class PrioritizeNode(Node):
    """Select the agenda under the constraints, rather than select and then trim.

    The tempting design ranks every issue, hands the list to a separate check,
    and lets that check delete what does not fit. It spends the cycle proposing
    work it already knew could not be done. Here the per-skill budget and the
    review capacity are part of the selection itself, so an item that could not
    be worked is never proposed.

    One constraint overrides the budget rather than competing with it: a
    safety-severity issue is always admitted. Nothing else in this graph is
    allowed to hold one back.
    """

    def __init__(self):
        super().__init__(
            "prioritize",
            reads=["residual_issues", "attention_budget", "capacity"],
            writes=["agenda"],
        )

    def run(self, view):
        residual = view.read("residual_issues", []) or []
        budget = view.read("attention_budget", {}) or {}
        capacity = int(view.read("capacity", 0) or 0)
        per_skill = dict(budget.get("per_skill") or {})

        live = [r for r in residual if r["residual_score"] > 0]
        live.sort(key=lambda r: (-r["residual_score"], r.get("id", "")))

        selected, used = [], defaultdict(int)

        for issue in live:  # safety first, and never budget-capped
            if issue.get("severity") == "safety":
                selected.append(dict(issue, admitted_by="safety_override"))
                used[issue.get("source_skill", "unknown")] += 1

        chosen_ids = {i.get("id") for i in selected}
        for issue in live:
            if issue.get("id") in chosen_ids:
                continue
            if len(selected) >= capacity:
                break
            skill = issue.get("source_skill", "unknown")
            if used[skill] >= per_skill.get(skill, 0):
                continue
            selected.append(dict(issue, admitted_by="budget"))
            used[skill] += 1
            chosen_ids.add(issue.get("id"))

        for issue in live:  # unused capacity spills to the best of what is left
            if len(selected) >= capacity:
                break
            if issue.get("id") in chosen_ids:
                continue
            selected.append(dict(issue, admitted_by="spillover"))
            used[issue.get("source_skill", "unknown")] += 1
            chosen_ids.add(issue.get("id"))

        selected.sort(key=lambda r: (r.get("severity") != "safety", -r["residual_score"]))
        view.write("agenda", selected)


class NetNode(Node):
    """Net the agenda before anything leaves the building.

    Two skills asking the same consultant about the same spec section on the
    same sheets is one question and two RFIs, and the second one costs a review
    cycle to answer identically. This node merges agenda items that would become
    one RFI, drops items already covered by an RFI in flight, and flags items
    where two skills are looking at the same element — which a person should
    reconcile before either question goes out, since the graph cannot tell
    whether they agree.
    """

    def __init__(self):
        super().__init__("net", reads=["agenda", "rfi_log"], writes=["net_agenda", "netting_report"])

    @staticmethod
    def _division(issue):
        refs = (issue.get("document_references") or {}).get("spec_sections") or []
        for section in refs:
            match = re.match(r"\s*(\d{2})", str(section))
            if match:
                return match.group(1)
        for sheet in (issue.get("location") or {}).get("sheets") or []:
            if sheet:
                return f"sheet-{str(sheet)[0].upper()}"
        return "unassigned"

    @staticmethod
    def _already_asked(issue, rfi_log):
        """Match an issue against RFIs in flight.

        Location alone is not enough. A door's fire rating and its hardware set
        cite the same sheet and the same spec section and are two different
        questions; suppressing the second because the first was asked is how a
        live conflict disappears quietly. A match therefore needs the same
        place AND the same subject. Same place, different subject is returned
        as a weak match — flagged for a person, never suppressed.
        """
        sheets = set((issue.get("location") or {}).get("sheets") or [])
        specs = set((issue.get("document_references") or {}).get("spec_sections") or [])
        terms = _subject_terms(issue)

        weak = None
        for entry in rfi_log:
            log_sheets = set(entry.get("sheets") or [])
            log_specs = set(entry.get("spec_sections") or [])
            co_located = bool((sheets & log_sheets) and (specs & log_specs)) or (
                bool(specs) and specs == log_specs and not sheets
            )
            if not co_located:
                continue
            log_terms = _subject_terms(entry)
            overlap = _jaccard(terms, log_terms) if log_terms else 0.0
            if overlap >= SAME_QUESTION_THRESHOLD:
                return entry.get("rfi_number"), "same_question", round(overlap, 4)
            weak = weak or (entry.get("rfi_number"), "same_location_only", round(overlap, 4))
        return weak

    def run(self, view):
        agenda = view.read("agenda", []) or []
        rfi_log = view.read("rfi_log", []) or []

        already_asked, possible_duplicates, open_items = [], [], []
        for issue in agenda:
            match = self._already_asked(issue, rfi_log)
            if match and match[1] == "same_question":
                already_asked.append(
                    {"id": issue.get("id"), "covered_by": match[0], "subject_overlap": match[2]}
                )
                continue
            if match:
                possible_duplicates.append(
                    {
                        "id": issue.get("id"),
                        "near": match[0],
                        "subject_overlap": match[2],
                        "note": "same sheet and spec section as an RFI in flight, different subject"
                        " — confirm it is genuinely a new question",
                    }
                )
            open_items.append(issue)

        # Bundle only what would genuinely be one RFI: same responsible division
        # AND the same sheet. Division alone would staple a corridor width on
        # A1.2 to a door rating on A3.1 because both are Division 08. A safety
        # issue is never bundled — it goes out on its own, now.
        bundles = defaultdict(list)
        for issue in open_items:
            sheets = sorted((issue.get("location") or {}).get("sheets") or [])
            if issue.get("severity") == "safety":
                key = ("!safety", issue.get("id"), sheets[0] if sheets else "")
            else:
                key = (self._division(issue), "", sheets[0] if sheets else "")
            bundles[key].append(issue)

        net_agenda, bundled = [], []
        for key in sorted(bundles):
            division, _, sheet = key
            members = sorted(bundles[key], key=lambda r: -r["residual_score"])
            lead = members[0]
            sheets = sorted({s for m in members for s in (m.get("location") or {}).get("sheets") or []})
            specs = sorted(
                {s for m in members for s in (m.get("document_references") or {}).get("spec_sections") or []}
            )
            if division == "!safety":
                label = "Safety — issued on its own"
                group = f"safety:{lead.get('id')}"
            else:
                label = DIVISION_NAMES.get(division, _fallback_label(division))
                group = f"{division}@{sheet}" if sheet else division
                if sheet:
                    label = f"{label} — {sheet}"
            net_agenda.append(
                {
                    "rfi_group": group,
                    "division_name": label,
                    "lead_issue": lead.get("id"),
                    "issue_ids": [m.get("id") for m in members],
                    "severity": min(
                        (m.get("severity", "info") for m in members),
                        key=lambda sev: SEVERITY_RANK.get(sev, 9),
                    ),
                    "score": round(sum(m["residual_score"] for m in members), 4),
                    "sheets": sheets,
                    "spec_sections": specs,
                    "source_skills": sorted({m.get("source_skill", "unknown") for m in members}),
                }
            )
            if len(members) > 1:
                bundled.append({"rfi_group": group, "merged": [m.get("id") for m in members]})

        by_element = defaultdict(list)
        for issue in open_items:
            for element in (issue.get("location") or {}).get("elements") or []:
                by_element[element].append(issue)
        reconcile = [
            {
                "element": element,
                "issue_ids": [i.get("id") for i in items],
                "source_skills": sorted({i.get("source_skill", "unknown") for i in items}),
                "note": "two skills reported on this element; confirm they agree before sending",
            }
            for element, items in sorted(by_element.items())
            if len({i.get("source_skill") for i in items}) > 1
        ]

        net_agenda.sort(key=lambda r: (SEVERITY_RANK.get(r["severity"], 9), -r["score"]))
        view.write("net_agenda", net_agenda)
        view.write(
            "netting_report",
            {
                "gross_items": len(agenda),
                "already_asked": already_asked,
                "possible_duplicates": possible_duplicates,
                "bundled": bundled,
                "reconcile": reconcile,
                "net_questions": len(net_agenda),
                "questions_saved": len(agenda) - len(net_agenda),
            },
        )


def _load_division_names():
    """Division labels from the shared CSI reference; the number alone if absent."""
    path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "reference", "csi_masterformat.yaml"
    )
    try:
        import yaml

        with open(path) as handle:
            data = yaml.safe_load(handle) or {}
        return {k: v.get("name", k) for k, v in (data.get("divisions") or {}).items()}
    except Exception:
        return {}


DIVISION_NAMES = _load_division_names()


def _fallback_label(division):
    """Readable name for a group with no CSI division to hang it on."""
    if division.startswith("sheet-"):
        return f"{division.split('-', 1)[1]}-series sheets (no spec section cited)"
    return "Unassigned (no spec section or sheet cited)"


def build_graph():
    return Graph(
        [ShrinkNode(), NeutralizeNode(), BudgetNode(), PrioritizeNode(), NetNode()],
        inputs=GRAPH_INPUTS,
    )
