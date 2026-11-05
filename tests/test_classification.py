"""Tests for scripts/classification.py — stdlib only, PyYAML optional."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))

import classification  # noqa: E402


class TestParse(unittest.TestCase):
    def test_uniclass_groups_at_three_segments(self):
        self.assertEqual(classification.parse("Ss_70_30_45"), ("uniclass", "Ss_70_30"))
        self.assertEqual(classification.parse("Ss_75_10_21 Data distribution"), ("uniclass", "Ss_75_10"))

    def test_uniclass_two_segment_reference_stays_at_two(self):
        self.assertEqual(classification.parse("PM_40"), ("uniclass", "PM_40"))
        self.assertEqual(classification.parse("Ss_25"), ("uniclass", "Ss_25"))

    def test_uniclass_found_inside_a_heading(self):
        self.assertEqual(classification.group_key("SECTION Ss_70_30_45 Low-voltage systems"), "Ss_70_30")

    def test_caws(self):
        self.assertEqual(classification.parse("V90 Section title"), ("caws", "CAWS-V"))
        self.assertEqual(classification.parse("W10"), ("caws", "CAWS-W"))

    def test_csi_legacy(self):
        self.assertEqual(classification.parse("08 71 00"), ("csi", "CSI-08"))
        self.assertEqual(classification.parse("26 05 19.13"), ("csi", "CSI-26"))
        self.assertEqual(classification.parse("08"), ("csi", "CSI-08"))

    def test_unrecognised_returns_none(self):
        for text in (None, "", "see drawings", "Hardware set 7"):
            self.assertIsNone(classification.parse(text), text)

    def test_uniclass_wins_over_a_leading_number(self):
        # A Uniclass code anywhere in the string is the authoritative reference.
        self.assertEqual(classification.group_key("01 Ss_70_30_45 LV systems"), "Ss_70_30")


class TestLabel(unittest.TestCase):
    def test_known_code_uses_reference_title(self):
        labels = {"Ss_70_30": "Electricity distribution systems", "Ss_70": "Electrical systems"}
        self.assertEqual(classification.label("Ss_70_30", labels), "Ss_70_30 Electricity distribution systems")

    def test_unknown_child_falls_back_to_parent_title(self):
        labels = {"Ss_70": "Electrical systems"}
        self.assertEqual(classification.label("Ss_70_99", labels), "Ss_70_99 (Electrical systems)")

    def test_unknown_code_is_labelled_by_code_only(self):
        self.assertEqual(classification.label("Pr_65_70", {}), "Pr_65_70")

    def test_legacy_systems_are_marked(self):
        self.assertIn("legacy UK", classification.label("CAWS-V", {}))
        self.assertIn("US spec", classification.label("CSI-08", {}))

    def test_reference_file_titles_load_when_yaml_is_available(self):
        try:
            import yaml  # noqa: F401
        except ImportError:
            self.skipTest("PyYAML not installed")
        labels = classification.load_labels()
        self.assertEqual(labels.get("Ss_75_10_21"), "Data distribution and telecommunications systems")
        self.assertEqual(labels.get("PM_70"), "Testing, commissioning and completion information")


if __name__ == "__main__":
    unittest.main()
