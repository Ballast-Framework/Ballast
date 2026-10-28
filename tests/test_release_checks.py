"""Synthetic release fixtures: tests never modify the real framework."""
import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_release.py"
SPEC = importlib.util.spec_from_file_location("check_release", SCRIPT)
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class ReleaseChecksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.control = dict(zip(release.CATALOG_COLUMNS, [
            "BAL-1.1", "1", "Example Domain", "Named owner", "Each asset has an accountable owner.",
            "T1", "Asset", "ALL", "Owner record", "Review the record."]))
        self.write_csv("controls/control-catalog.csv", release.CATALOG_COLUMNS, [self.control])
        self.write_csv("guides/assessment-template.csv", release.SHARED_ASSESSMENT, [self.control])
        self.mapping = dict(zip(release.MAPPING_COLUMNS, ["BAL-1.1", "nist_ai_rmf", "1.0", "GOVERN 1.1", "Governance"]))
        self.write_csv("mappings/control-mappings.csv", release.MAPPING_COLUMNS, [self.mapping])
        self.write("mappings/crosswalk.md", "# Crosswalk\n\n<!-- GENERATED DOMAIN TABLES BELOW -->\n\n## Domain 1\n\n| Framework | References (Ballast controls) |\n|---|---|\n| NIST AI RMF 1.0 | GOVERN 1.1 Governance (1.1) |\n")
        table = "| ID | Control | Requirement | Tier | Scope | Applies to |\n|---|---|---|---|---|---|\n| " + " | ".join(self.control[k] for k in release.TABLE_FIELDS) + " |\n"
        self.write("controls/control-catalog.md", "# Catalog\n\n" + table)
        self.write("framework/domains/01-example.md", "# Example Domain\n\n" + table)
        self.write("README.md", "# Ballast\n\nVersion: 1.0.0; v1.0.0\n\n![Version: 1.0.0](https://img.shields.io/badge/version-1.0.0-blue.svg)\n\n"
                   "| # | Domain | Focus | Controls | T1 | T2 | T3 |\n|---|---|---|---|---|---|---|\n"
                   "| 1 | [Example](framework/domains/01-example.md#example-domain) | Ownership | 1 | 1 | 0 | 0 |\n"
                   "| | **Total** | | **1** | **1** | **0** | **0** |\n")
        self.write("CITATION.cff", 'cff-version: 1.2.0\nversion: "1.0.0"\ndate-released: "2026-10-25"\nrepository-code: "https://github.com/example/ballast"\n')
        self.write("CHANGELOG.md", "# Changelog\n\n## [1.0.0] - 2026-10-25\n")

    def write(self, name, content):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def write_csv(self, name, columns, rows):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)

    def findings(self):
        return release.ReleaseCheck(self.root).run()

    def assertFinding(self, text):
        self.assertTrue(any(text in f for f in self.findings()), text)

    def test_consistent_release_passes_without_mutation(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(self.findings(), [])
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_duplicate_catalog_control_fails(self):
        self.write_csv("controls/control-catalog.csv", release.CATALOG_COLUMNS, [self.control, self.control])
        self.assertFinding("duplicate control ID")

    def test_domain_requirement_drift_fails(self):
        path = self.root / "framework/domains/01-example.md"
        self.write(path.relative_to(self.root), path.read_text().replace("Each asset has an accountable owner.", "No owner is required."))
        self.assertFinding("differs from catalog CSV in requirement")

    def test_non_control_tables_are_not_misclassified(self):
        path = self.root / "framework/domains/01-example.md"
        self.write(path.relative_to(self.root), path.read_text() + "\n| ID | Evidence |\n|---|---|\n| BAL-1.1 | Owner record |\n")
        self.assertEqual(self.findings(), [])

    def test_mapping_unknown_id_and_duplicates_fail(self):
        self.write_csv("mappings/control-mappings.csv", release.MAPPING_COLUMNS,
                       [self.mapping, self.mapping, dict(self.mapping, control_id="BAL-9.9")])
        self.assertFinding("duplicate mapping key")
        self.assertFinding("unknown control BAL-9.9")

    def test_csv_width_error_is_reported(self):
        path = self.root / "guides/assessment-template.csv"
        with path.open("a", encoding="utf-8") as handle:
            handle.write("broken,row\n")
        self.assertFinding("CSV has 2 cells")

    def test_broken_image_and_anchor_fail(self):
        path = self.root / "README.md"
        self.write("README.md", path.read_text() + "\n![Figure](assets/missing.png)\n[Wrong](framework/domains/01-example.md#absent)\n")
        self.assertFinding("missing local link/image")
        self.assertFinding("missing Markdown anchor")

    def test_release_date_mismatch_and_commented_field_fail(self):
        self.write("CHANGELOG.md", "## [1.0.0] - 2026-10-24\n")
        self.assertFinding("first dated release must match")
        path = self.root / "CITATION.cff"
        self.write("CITATION.cff", path.read_text().replace("date-released:", "# date-released:"))
        self.assertFinding("still commented out")

    def test_name_and_real_placeholder_fail_but_examples_pass(self):
        self.write("SECURITY.md", "Contact **[SECURITY CONTACT]**.\n")
        self.write("AUTHORS.md", "Avi Nikum\n")
        self.assertFinding("unresolved publication placeholder")
        self.assertFinding("author name needs")
        self.write("SECURITY.md", "Contact [Avishkar (Avi) Nikum](https://example.test/avi).\n")
        self.write("AUTHORS.md", "Avishkar (Avi) Nikum\n\nUse `BAL-<domain>.<n>` and `YYYY-MM-DD` in templates.\n```text\n[RELEASE DATE]\n```\n")
        self.assertEqual(self.findings(), [])

    def test_readme_counts_are_derived_not_hardcoded(self):
        path = self.root / "README.md"
        self.write("README.md", path.read_text().replace("**1** | **1**", "**2** | **1**"))
        self.assertFinding("total/tier counts differ")

    def test_release_tag_must_match_citation_version(self):
        self.assertEqual(release.ReleaseCheck(self.root, tag="v1.0.0").run(), [])
        errors = release.ReleaseCheck(self.root, tag="v1.1.0").run()
        self.assertTrue(any("Release tag v1.1.0 does not match" in e for e in errors))

    def test_valid_mapping_edit_requires_crosswalk_update(self):
        self.write_csv("mappings/control-mappings.csv", release.MAPPING_COLUMNS,
                       [dict(self.mapping, ref_id="GOVERN 1.2")])
        self.assertFinding("generated domain tables differ from mappings CSV")

    def test_stale_owasp_coverage_is_detected(self):
        self.write_csv("mappings/control-mappings.csv", release.MAPPING_COLUMNS,
                       [dict(self.mapping, framework="owasp_llm_2026", framework_version="2026", ref_id="LLM01", ref_name="Prompt Injection")])
        self.write("mappings/crosswalk.md", "# Crosswalk\n\n## Domain 1\n\n| Framework | References (Ballast controls) |\n|---|---|\n| OWASP Top 10 for LLM Applications 2026 | LLM01 Prompt Injection (1.1) |\n\n## Coverage: OWASP Top 10 for LLM Applications 2026\n\n| ID | Risk | Controls |\n|---|---|---|\n| LLM01 | Prompt Injection | 1.9 |\n")
        self.assertFinding("OWASP coverage tables differ from mappings CSV")

    def test_backticked_publication_placeholder_is_not_exempt(self):
        path = self.root / "README.md"
        self.write("README.md", path.read_text() + "\nRelease date: `[RELEASE DATE]`\nPresenter: [PRESENTER NAME]\n[SECURITY.md](SECURITY.md)\n")
        self.write("SECURITY.md", "# Security\n")
        findings = self.findings()
        placeholders = [e for e in findings if "unresolved publication placeholder" in e]
        self.assertEqual(len(placeholders), 2)

    def test_version_badge_url_must_match_even_when_alt_is_correct(self):
        path = self.root / "README.md"
        self.write("README.md", path.read_text().replace("badge/version-1.0.0-blue", "badge/version-9.9.9-blue"))
        self.assertFinding("actual version badge URL does not match")

    def test_applies_to_and_or_grammar_and_known_tags(self):
        for tag in release.TAGS:
            self.assertTrue(release.applies(tag, {tag}))
        self.assertTrue(release.applies("BUILT+RAG, AGENT+ACT", {"BUILT", "RAG"}))
        self.assertTrue(release.applies("BUILT+RAG, AGENT+ACT", {"AGENT", "ACT"}))
        self.assertFalse(release.applies("BUILT+RAG, AGENT+ACT", {"BUILT", "ACT"}))
        self.assertTrue(release.applies("ALL", set()))

    def test_malformed_applicability_is_rejected(self):
        for bad in ("", "AGNET", "AGENT,", ",AGENT", "AGENT,,ACT", "AGENT+", "+ACT",
                    "BUILT++RAG", "AGENT OR ACT", "AGENT|ACT", "(AGENT)", "agent",
                    "ALL,AGENT", "ALL+AGENT"):
            with self.subTest(expression=bad), self.assertRaises(ValueError):
                release.parse_expression(bad)

    def test_synchronized_unknown_tag_still_fails(self):
        self.control["applies_to"] = "AGNET"
        self.write_csv("controls/control-catalog.csv", release.CATALOG_COLUMNS, [self.control])
        self.write_csv("guides/assessment-template.csv", release.SHARED_ASSESSMENT, [self.control])
        for name in ("controls/control-catalog.md", "framework/domains/01-example.md"):
            self.write(name, (self.root / name).read_text().replace("| ALL |", "| AGNET |"))
        findings = self.findings()
        self.assertTrue(any("invalid applies_to expression" in error for error in findings))
        self.assertFalse(any("differs from catalog" in error for error in findings))

    def test_documented_vocabulary_must_match_supported_tags(self):
        rows = "\n".join(f"| {tag} | Meaning |" for tag in sorted(release.TAGS))
        self.write("guides/tiering.md", "| Tag | Applies when the asset... |\n|---|---|\n" + rows + "\n")
        self.assertEqual(self.findings(), [])
        self.write("guides/tiering.md", (self.root / "guides/tiering.md").read_text().replace("| AGENT |", "| AGNET |"))
        self.assertFinding("documented tag vocabulary differs")

    def test_linked_control_rows_and_control_tier_headers_pass(self):
        for name in ("controls/control-catalog.md", "framework/domains/01-example.md"):
            text = (self.root / name).read_text()
            text = text.replace("| Tier |", "| Control Tier |")
            text = text.replace("| BAL-1.1 |", '| <a id="bal-1-1"></a>[BAL-1.1](#bal-1-1) |')
            text = text.replace("| T1 |", '| <a id="t1"></a>[T1](#t1) |')
            self.write(name, text)
        self.assertEqual(self.findings(), [])

    def test_scope_and_domain_counts_outside_readme_are_checked(self):
        self.write("guides/tiering.md", "| Scope | Controls | T1 | T2 | T3 |\n|---|---|---|---|---|\n| Asset | 2 | 1 | 0 | 0 |\n| Total | 1 | 1 | 0 | 0 |\n")
        self.assertFinding("published domain/scope/tier counts differ")
        self.write("guides/tiering.md", "| # | Domain | Controls | T1 | T2 | T3 |\n|---|---|---|---|---|---|\n| 1 | Example | 1 | 0 | 1 | 0 |\n| | Total | 1 | 1 | 0 | 0 |\n")
        self.assertFinding("published domain/scope/tier counts differ")

    def test_domain_intro_count_is_checked(self):
        name = "framework/domains/01-example.md"
        self.write(name, (self.root / name).read_text() + "\n2 controls (T1: 1, T2: 1, T3: 0)\n")
        self.assertFinding("domain introduction counts differ")

    def test_example_counts_derive_from_tags_and_tier_changes(self):
        self.write("guides/tiering.md", "| Asset type | Tags | Asset T1 | Added T2 if rated High | T3 (A4 only) |\n|---|---|---|---|---|\n| Example | AGENT | 1 | 0 | 0 |\n")
        self.assertEqual(self.findings(), [])
        changed = dict(self.control, tier="T2")
        check = release.ReleaseCheck(self.root)
        check.published_counts({changed["control_id"]: changed}, {"1": "Example Domain"})
        self.assertTrue(any("example tier counts differ" in e for e in check.errors))
        self.write("guides/tiering.md", (self.root / "guides/tiering.md").read_text().replace("| 1 | 0 | 0 |", "| 0 | 1 | 0 |"))
        check = release.ReleaseCheck(self.root)
        check.published_counts({changed["control_id"]: changed}, {"1": "Example Domain"})
        self.assertFalse(any("example tier counts differ" in e for e in check.errors))

    def test_example_and_clause_requires_both_tags(self):
        self.write("guides/tiering.md", "| Asset type | Tags | Asset T1 | Added T2 if rated High | T3 (A4 only) |\n|---|---|---|---|---|\n| Example | BUILT | 1 | 0 | 0 |\n")
        changed = dict(self.control, applies_to="BUILT+RAG")
        check = release.ReleaseCheck(self.root)
        check.published_counts({changed["control_id"]: changed}, {"1": "Example Domain"})
        self.assertTrue(any("example tier counts differ" in e for e in check.errors))

    def test_risk_example_requires_only_the_selected_control_tiers(self):
        self.write("guides/tiering.md", "| Asset | Tags | Highest autonomy | Rules met | Rating | Asset controls required |\n|---|---|---|---|---|---|\n| Example | AGENT | A0 | None | Low or Medium | 1 T1 |\n")
        extra = dict(self.control, control_id="BAL-1.2", tier="T2")
        controls = {r["control_id"]: r for r in (self.control, extra)}
        check = release.ReleaseCheck(self.root)
        check.published_counts(controls, {"1": "Example Domain"})
        self.assertFalse(any("risk-rated example counts differ" in e for e in check.errors))
        self.write("guides/tiering.md", (self.root / "guides/tiering.md").read_text().replace("Low or Medium", "High"))
        check = release.ReleaseCheck(self.root)
        check.published_counts(controls, {"1": "Example Domain"})
        self.assertTrue(any("risk-rated example counts differ" in e for e in check.errors))

    def test_baseline_prose_is_derived_from_scope_and_applicability(self):
        self.write("guides/adoption.md", "That is 1 unconditional controls (1 Program, 0 Vendor) and 0 conditional ones.\n")
        check = release.ReleaseCheck(self.root)
        check.published_counts({self.control["control_id"]: self.control}, {"1": "Example Domain"})
        self.assertTrue(any("baseline scope breakdown differs" in e for e in check.errors))
        changed = dict(self.control, scope="Program")
        check = release.ReleaseCheck(self.root)
        check.published_counts({changed["control_id"]: changed}, {"1": "Example Domain"})
        self.assertFalse(any("baseline" in e for e in check.errors))

    def test_current_changelog_counts_checked_but_history_preserved(self):
        self.write("CHANGELOG.md", "## [1.0.0] - 2026-10-25\n\n1 controls in 1 domains\n\n## [0.1.0] - 2025-01-01\n\n99 controls in 8 domains\n")
        self.assertEqual(self.findings(), [])
        self.write("CHANGELOG.md", (self.root / "CHANGELOG.md").read_text().replace("1 controls in 1 domains", "2 controls in 1 domains"))
        self.assertFinding("published overall control/domain count differs")

    def test_worked_example_selection_and_count_are_both_verified(self):
        controls = {"BAL-1.1": self.control,
                    "BAL-1.2": dict(self.control, control_id="BAL-1.2", applies_to="RAG"),
                    "BAL-1.3": dict(self.control, control_id="BAL-1.3", tier="T2"),
                    "BAL-1.4": dict(self.control, control_id="BAL-1.4", tier="T2", applies_to="RAG")}
        sample = """# Worked example

**Tags: AGENT.**

### Asset T1: 1 controls
| Control | Name | Matched clause |
|---|---|---|
| BAL-1.1 | Named owner | ALL |

### Asset T1 controls that do not apply: 1
| Control | Name | Needs |
|---|---|---|
| BAL-1.2 | Retrieval | RAG |

### Asset T2: 1 controls
| Domain | Controls |
|---|---|
| 1 | BAL-1.3 Elevated owner |

One asset T2 controls do not apply: BAL-1.4 (RAG).

### T3

**Result: 2 Asset rows apply to this agent, 1 at T1 and 1 at T2, out of 4 controls.**
"""
        self.write("guides/worked-example.md", sample)
        check = release.ReleaseCheck(self.root)
        check.worked_example(controls, [])
        self.assertEqual(check.errors, [])
        # A same-sized but wrong selection must fail, even when counts still match.
        self.write("guides/worked-example.md", sample.replace("| BAL-1.1 |", "| BAL-1.2 |"))
        check = release.ReleaseCheck(self.root)
        check.worked_example(controls, [])
        self.assertTrue(any("T1 applicable control selection differs" in e for e in check.errors))
        self.write("guides/worked-example.md", sample.replace("Asset T1: 1", "Asset T1: 2"))
        check = release.ReleaseCheck(self.root)
        check.worked_example(controls, [])
        self.assertTrue(any("heading count differs" in e for e in check.errors))


if __name__ == "__main__":
    unittest.main()
