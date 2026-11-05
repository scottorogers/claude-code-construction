#!/usr/bin/env python3
"""
classification.py — Read a specification section reference and say which
work group it belongs to.

UK specs are numbered in Uniclass 2015 (NBS Chorus), older UK specs in NBS
CAWS, and US specs in CSI MasterFormat. A project can contain all three (a US
manufacturer's spec bound into a UK manual), so the parser recognises each
and never guesses between them:

  Uniclass 2015   Ss_70_30_45, Ss_75_10_21, PM_40, Pr_65_70_48
                  -> group at the first three segments ("Ss_70_30"); falls back
                     to two ("Ss_70") when that is all the reference gives
  NBS CAWS        V90, W10, Y61  -> "CAWS-V"
  CSI MasterFormat 08 71 00, 26 05 19, or a bare "08" -> "CSI-08"

Anything else is unrecognised and returns None — the caller decides what an
unclassified issue means. Labels come from reference/uniclass2015.yaml; a
code not in that file is labelled by its code alone rather than by a name
made up here.
"""

import os
import re

_UNICLASS = re.compile(
    r"(?<![A-Za-z0-9])(Ss|Pr|PM|EF|En|SL|Ac|Co|Ma|Ro|FI|PC|Te|Zz)_(\d{2})(?:_(\d{2}))?(?:_(\d{2}))?(?:_(\d{2}))?(?![0-9])"
)
# CAWS sections are one capital letter + two digits, written alone or before a
# title: "V90", "W10 Telecommunications". Requiring the match at the start of
# the string keeps it from firing on sheet numbers buried in prose.
_CAWS = re.compile(r"^\s*([A-Z])(\d{2})(?![0-9_])")
_CSI = re.compile(r"^\s*(\d{2})(?:[\s.]?\d{2}){0,3}(?![0-9_])")

DEFAULT_REFERENCE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "reference", "uniclass2015.yaml"
)


def parse(reference):
    """Return (system, group_key) for a section reference, or None.

    system is one of "uniclass", "caws", "csi".
    """
    if reference is None:
        return None
    text = str(reference)
    match = _UNICLASS.search(text)
    if match:
        table, *parts = match.groups()
        segments = [p for p in parts if p]
        depth = 2 if len(segments) >= 2 else 1
        return "uniclass", "_".join([table] + segments[:depth])
    match = _CAWS.match(text)
    if match:
        return "caws", f"CAWS-{match.group(1)}"
    match = _CSI.match(text)
    if match:
        return "csi", f"CSI-{match.group(1)}"
    return None


def group_key(reference):
    """The grouping key alone, or None if the reference is unrecognised."""
    parsed = parse(reference)
    return parsed[1] if parsed else None


def load_labels(path=DEFAULT_REFERENCE):
    """Map every Uniclass code in the reference file to its title.

    Returns {} if PyYAML or the file is missing — callers then label groups by
    code, which is less readable but never wrong.
    """
    try:
        import yaml

        with open(path) as handle:
            data = yaml.safe_load(handle) or {}
    except Exception:
        return {}
    labels = {}
    for code, entry in (data.get("groups") or {}).items():
        labels[code] = entry.get("name", code)
        for level in ("children", "grandchildren"):
            labels.update(entry.get(level) or {})
    for code, entry in (data.get("pm_groups") or {}).items():
        labels[code] = entry.get("name", code)
    return labels


def label(key, labels):
    """Readable label for a group key produced by group_key()."""
    if key is None:
        return "Unclassified"
    if key.startswith("CAWS-"):
        return f"NBS CAWS group {key[5:]} (legacy UK spec)"
    if key.startswith("CSI-"):
        return f"CSI Division {key[4:]} (US spec)"
    if key in labels:
        return f"{key} {labels[key]}"
    parent = "_".join(key.split("_")[:2])
    if parent in labels:
        return f"{key} ({labels[parent]})"
    return key
