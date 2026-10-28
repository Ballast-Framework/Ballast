#!/usr/bin/env python3
"""Read-only, standard-library release checks for Ballast (Python 3.10+)."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import date
import html
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

CONTROL_ID = re.compile(r"\bBAL-\d+\.\d+\b")
CATALOG_COLUMNS = ("control_id", "domain_number", "domain", "control", "requirement", "tier", "scope", "applies_to", "evidence", "guidance")
MAPPING_COLUMNS = ("control_id", "framework", "framework_version", "ref_id", "ref_name")
SHARED_ASSESSMENT = ("control_id", "domain", "control", "tier", "scope", "applies_to")
TABLE_FIELDS = ("control_id", "control", "requirement", "tier", "scope", "applies_to")
PUBLICATION_MARKERS = re.compile(r"\[(?:AUTHOR|PRESENTER|RELEASE|REPOSITORY|GITHUB|QR|SECURITY|CONDUCT|DISCLOSURE|INSERT)(?:[ _-][A-Z0-9 _-]+)?\]|https://github\.com/OWNER/REPOSITORY|\b(?:TBD|FIXME)\b|\bTODO before tagging\b")
SEMVER = re.compile(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?")
TAGS = frozenset("ALL BUILT AGENT ACT AUTO EXEC RAG MEM UNTRUSTED EXT MULTI MODEL INFRA CODE ENDPOINT PUBLIC LOWCODE".split())
TIERS = ("T1", "T2", "T3")


def parse_expression(expression: str) -> tuple[frozenset[str], ...]:
    """Comma-separated OR clauses, with plus-separated AND terms in each clause."""
    clauses = []
    for clause in expression.split(","):
        terms = clause.strip().split("+")
        if any(not term.strip() for term in terms):
            raise ValueError("empty clause or dangling operator")
        tokens = [term.strip() for term in terms]
        unknown = set(tokens) - TAGS
        if unknown:
            raise ValueError("unknown tag or unsupported syntax: " + ", ".join(sorted(unknown)))
        clauses.append(frozenset(tokens))
    if any("ALL" in clause for clause in clauses) and clauses != [frozenset({"ALL"})]:
        raise ValueError("ALL must stand alone")
    return tuple(clauses)


def applies(expression: str, tags: set[str]) -> bool:
    try:
        return any(clause == {"ALL"} or clause <= tags for clause in parse_expression(expression))
    except ValueError:
        return False  # The catalog pass reports malformed expressions separately.


def visible_lines(text: str):
    """Skip fenced examples; keep source line numbers for diagnostics."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        found = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if found:
            mark = found.group(1)
            if fence is None:
                fence = (mark[0], len(mark))
            elif mark[0] == fence[0] and len(mark) >= fence[1]:
                fence = None
            continue
        if fence is None:
            yield number, line


def cell(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"<[^>]*>", "", value)
    return " ".join(html.unescape(value).replace(r"\|", "|").replace("`", "").replace("**", "").strip("*").split())


def tables(text: str):
    """Yield a header and its data rows, ignoring Markdown alignment rules."""
    header, rows = None, []
    for number, line in list(visible_lines(text)) + [(0, "")]:
        if not line.lstrip().startswith("|"):
            if header is not None:
                yield header, rows
            header, rows = None, []
            continue
        values = [cell(c) for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if header is None:
            header = values
        elif not all(re.fullmatch(r":?-+:?", v) for v in values):
            rows.append((number, values))


def table_rows(text: str):
    for number, line in visible_lines(text):
        if line.lstrip().startswith("|"):
            yield number, [cell(c) for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def anchors(text: str) -> set[str]:
    result, counts = set(), Counter()
    for _, line in visible_lines(text):
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match:
            title = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", match.group(1))
            title = re.sub(r"<[^>]*>", "", html.unescape(title)).replace("`", "").replace("*", "")
            slug = re.sub(r"[^\w\s-]", "", title.lower()).replace(" ", "-")
            suffix = counts[slug]
            counts[slug] += 1
            result.add(slug + (f"-{suffix}" if suffix else ""))
        result.update(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)', line, re.I))
    return result


def local_destinations(text: str):
    for number, line in visible_lines(text):
        line = re.sub(r"`+[^`]*`+", "", line)
        # This includes image destinations. Nested badge destinations are
        # individually discovered where possible; external targets are ignored.
        for match in re.finditer(r"!?\[[^\]]*\]\(\s*<?([^\s)>]+)>?(?:\s+[^)]*)?\)", line):
            yield number, match.group(1)
        ref = re.match(r"^\s{0,3}\[[^\]]+\]:\s*<?([^\s>]+)", line)
        if ref:
            yield number, ref.group(1)


def check_local_links(root: Path, relative: str, text: str, texts: dict[str, str]) -> list[str]:
    errors = []
    for number, target in local_destinations(text):
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or target.startswith("//"):
            continue
        dest = (root / unquote(parsed.path.lstrip("/")) if parsed.path.startswith("/")
                else root / relative if not parsed.path else (root / relative).parent / unquote(parsed.path))
        dest = dest.resolve()
        if not dest.is_relative_to(root.resolve()):
            errors.append(f"{relative}:{number}: local link escapes the repository: {target}")
        elif not dest.exists():
            errors.append(f"{relative}:{number}: missing local link/image: {target}")
        elif parsed.fragment and dest.suffix.lower() == ".md":
            name = dest.relative_to(root.resolve()).as_posix()
            content = texts.get(name)
            if content is None:
                content = dest.read_text(encoding="utf-8")
            if unquote(parsed.fragment) not in anchors(content):
                errors.append(f"{relative}:{number}: missing Markdown anchor: {target}")
    return errors


class ReleaseCheck:
    def __init__(self, root: Path, tag: str | None = None):
        self.root = root.resolve()
        self.tag = tag
        self.errors: list[str] = []
        self.notes: list[str] = []
        self.texts: dict[str, str] = {}
        self.summary: dict[str, object] = {}

    def fail(self, message: str):
        self.errors.append(message)

    def text(self, name: str) -> str:
        if name in self.texts:
            return self.texts[name]
        try:
            self.texts[name] = (self.root / name).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            self.fail(f"{name}: cannot read UTF-8 source ({type(exc).__name__})")
            self.texts[name] = ""
        return self.texts[name]

    def read_csv(self, name: str, required=()):
        path = self.root / name
        try:
            with path.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.reader(handle)
                header = next(reader, [])
                if len(set(header)) != len(header) or not header or any(not h for h in header):
                    self.fail(f"{name}: invalid or duplicate CSV headers")
                missing = set(required) - set(header)
                if missing:
                    self.fail(f"{name}: missing columns: {', '.join(sorted(missing))}")
                rows = []
                for values in reader:
                    number = reader.line_num
                    if len(values) != len(header):
                        self.fail(f"{name}:{number}: CSV has {len(values)} cells, expected {len(header)}")
                        continue
                    row = dict(zip(header, values))
                    for key in required:
                        if not row.get(key, "").strip():
                            self.fail(f"{name}:{number}: empty required field {key}")
                    rows.append((number, row))
                return header, rows
        except (OSError, UnicodeError, csv.Error) as exc:
            self.fail(f"{name}: cannot read CSV ({type(exc).__name__})")
            return [], []

    def control_tables(self, name: str, expected: dict[str, dict]):
        actual = {}
        active = False
        parsed = []
        for number, line in visible_lines(self.text(name)):
            if not line.lstrip().startswith("|"):
                active = False
                continue
            values = [cell(c) for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
            if values in (["ID", "Control", "Requirement", "Tier", "Scope", "Applies to"],
                          ["ID", "Control", "Requirement", "Control Tier", "Scope", "Applies to"]):
                active = True
                continue
            if active:
                parsed.append((number, values))
        for number, values in parsed:
            if not values or not CONTROL_ID.fullmatch(values[0]):
                continue
            key = values[0]
            if len(values) != len(TABLE_FIELDS):
                self.fail(f"{name}:{number}: control table has an unexpected column count")
                continue
            if key in actual:
                self.fail(f"{name}:{number}: duplicate control row {key}")
            actual[key] = values
            if key not in expected:
                self.fail(f"{name}:{number}: unexpected control row {key}")
                continue
            wanted = [cell(expected[key].get(field, "")) for field in TABLE_FIELDS]
            if values != wanted:
                changed = [field for field, left, right in zip(TABLE_FIELDS, values, wanted) if left != right]
                self.fail(f"{name}:{number}: {key} differs from catalog CSV in {', '.join(changed)}")
        if set(actual) != set(expected):
            self.fail(f"{name}: table control set differs from catalog (missing {len(set(expected)-set(actual))}, extra {len(set(actual)-set(expected))})")

    def catalog_and_data(self):
        _, records = self.read_csv("controls/control-catalog.csv", CATALOG_COLUMNS)
        controls = {}
        domain_names = {}
        for number, row in records:
            key = row.get("control_id", "")
            if not CONTROL_ID.fullmatch(key):
                self.fail(f"controls/control-catalog.csv:{number}: invalid control ID {key}")
            if key in controls:
                self.fail(f"controls/control-catalog.csv:{number}: duplicate control ID {key}")
            controls[key] = row
            if row.get("tier") not in ("T1", "T2", "T3"):
                self.fail(f"controls/control-catalog.csv:{number}: invalid tier")
            if row.get("scope") not in ("Asset", "Program", "Vendor"):
                self.fail(f"controls/control-catalog.csv:{number}: invalid scope")
            try:
                parse_expression(row.get("applies_to", ""))
            except ValueError as exc:
                self.fail(f"controls/control-catalog.csv:{number}: invalid applies_to expression ({exc})")
            domain = row.get("domain_number", "")
            if not domain.isdigit() or not key.startswith(f"BAL-{domain}."):
                self.fail(f"controls/control-catalog.csv:{number}: domain number does not match ID")
            if domain in domain_names and domain_names[domain] != row.get("domain"):
                self.fail(f"controls/control-catalog.csv:{number}: inconsistent domain title")
            domain_names[domain] = row.get("domain")
        if not controls:
            self.fail("controls/control-catalog.csv: catalog must contain controls")
        self.control_tables("controls/control-catalog.md", controls)
        seen_domains = set()
        for path in sorted((self.root / "framework/domains").glob("*.md")):
            name = path.relative_to(self.root).as_posix()
            match = re.match(r"(\d+)-", path.name)
            if not match:
                self.fail(f"{name}: domain filename needs a numeric prefix")
                continue
            domain = str(int(match.group(1)))
            if domain in seen_domains:
                self.fail(f"{name}: repeated domain number")
            seen_domains.add(domain)
            self.control_tables(name, {k: r for k, r in controls.items() if r.get("domain_number") == domain})
            for number, line in visible_lines(self.text(name)):
                count = re.fullmatch(r"(\d+) controls \(T1: (\d+), T2: (\d+), T3: (\d+)\)", cell(line))
                rows = [r for r in controls.values() if r.get("domain_number") == domain]
                expected = [len(rows)] + [sum(r.get("tier") == tier for r in rows) for tier in TIERS]
                if count and list(map(int, count.groups())) != expected:
                    self.fail(f"{name}:{number}: domain introduction counts differ from CSV")
        if seen_domains != set(domain_names):
            self.fail("framework/domains: domain files do not match catalog domains")
        _, assessment = self.read_csv("guides/assessment-template.csv", SHARED_ASSESSMENT)
        assessment_ids = []
        for number, row in assessment:
            key = row.get("control_id", "")
            assessment_ids.append(key)
            if key not in controls or any(row.get(field) != controls[key].get(field) for field in SHARED_ASSESSMENT):
                self.fail(f"guides/assessment-template.csv:{number}: control metadata differs from catalog")
        if len(set(assessment_ids)) != len(assessment_ids) or set(assessment_ids) != set(controls):
            self.fail("guides/assessment-template.csv: IDs must match catalog exactly once")
        _, mappings = self.read_csv("mappings/control-mappings.csv", MAPPING_COLUMNS)
        mapped, keys = set(), set()
        for number, row in mappings:
            control = row.get("control_id", "")
            mapped.add(control)
            if control not in controls:
                self.fail(f"mappings/control-mappings.csv:{number}: unknown control {control}")
            key = tuple(row.get(field) for field in MAPPING_COLUMNS[:-1])
            if key in keys:
                self.fail(f"mappings/control-mappings.csv:{number}: duplicate mapping key")
            keys.add(key)
        if mapped != set(controls):
            self.fail("mappings/control-mappings.csv: every catalog control needs at least one mapping")
        self.generated_crosswalk(mappings, controls)
        checked = {"controls/control-catalog.csv", "guides/assessment-template.csv", "mappings/control-mappings.csv"}
        for path in self.root.rglob("*.csv"):
            name = path.relative_to(self.root).as_posix()
            if name not in checked:
                self.read_csv(name)  # Intentional blank template cells are allowed.
        self.summary.update(controls=len(controls), domains=len(domain_names), mappings=len(mappings),
                            tiers=dict(Counter(r.get("tier") for r in controls.values())),
                            scopes=dict(Counter(r.get("scope") for r in controls.values())))
        self.check_readme_counts(controls, domain_names)
        self.published_counts(controls, domain_names)
        return controls

    def generated_crosswalk(self, mappings, controls):
        labels = {
            "owasp_llm_2026": "OWASP Top 10 for LLM Applications {version}",
            "owasp_asi_2026": "OWASP Top 10 for Agentic Applications {version}",
            "atlas": "MITRE ATLAS (data release {version})",
            "nist_ai_rmf": "NIST AI RMF {version}",
            "iso_42001": "ISO/IEC 42001:{version} Annex A",
        }
        expected, coverage = {}, {}
        short_sort = lambda key: tuple(int(n) for n in key.split("."))
        for _, row in mappings:
            key = row.get("control_id", "")
            if key not in controls or row.get("framework") not in labels:
                continue
            label = labels[row["framework"]].format(version=row["framework_version"])
            domain = controls[key]["domain_number"]
            short = key.removeprefix("BAL-")
            expected.setdefault((domain, label), {}).setdefault(row["ref_id"] + " " + row["ref_name"], set()).add(short)
            if row["framework"].startswith("owasp_"):
                coverage.setdefault((label, row["ref_id"]), set()).add(short)
        actual, actual_coverage = {}, {}
        domain, coverage_label = None, None
        for number, line in visible_lines(self.text("mappings/crosswalk.md")):
            heading = re.match(r"^## Domain (\d+)\s*$", line)
            if heading:
                domain, coverage_label = heading.group(1), None
            elif line.startswith("## Coverage: "):
                domain, coverage_label = None, line.removeprefix("## Coverage: ").strip()
            elif line.startswith("## "):
                domain, coverage_label = None, None
            if not line.startswith("|"):
                continue
            values = [cell(c) for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
            if domain is not None and len(values) == 2 and values[0] not in ("Framework", "---"):
                groups = Counter(values[1].split("; "))
                key = (domain, values[0])
                if key in actual:
                    self.fail(f"mappings/crosswalk.md:{number}: duplicate generated framework row")
                actual[key] = groups
            elif coverage_label and len(values) == 3 and re.fullmatch(r"(?:LLM|ASI)\d+", values[0]):
                key = (coverage_label, values[0])
                if key in actual_coverage:
                    self.fail(f"mappings/crosswalk.md:{number}: duplicate OWASP coverage row")
                actual_coverage[key] = set(re.findall(r"\b\d+\.\d+\b", values[2]))
        wanted = {key: Counter(caption + " (" + ", ".join(sorted(ids, key=short_sort)) + ")" for caption, ids in groups.items()) for key, groups in expected.items()}
        if actual != wanted:
            self.fail("mappings/crosswalk.md: generated domain tables differ from mappings CSV")
        if actual_coverage != coverage:
            self.fail("mappings/crosswalk.md: OWASP coverage tables differ from mappings CSV")

    def check_readme_counts(self, controls: dict, domain_names: dict):
        seen = set()
        totals = [len(controls)] + [sum(r.get("tier") == t for r in controls.values()) for t in ("T1", "T2", "T3")]
        found_total = False
        for number, values in table_rows(self.text("README.md")):
            if len(values) != 7:
                continue
            if values[0].isdigit():
                domain = values[0]
                seen.add(domain)
                rows = [r for r in controls.values() if r.get("domain_number") == domain]
                expected = [len(rows)] + [sum(r.get("tier") == tier for r in rows) for tier in ("T1", "T2", "T3")]
                if values[3:] != [str(n) for n in expected]:
                    self.fail(f"README.md:{number}: domain/tier counts differ from CSV")
            elif values[1] == "Total":
                found_total = True
                if values[3:] != [str(n) for n in totals]:
                    self.fail(f"README.md:{number}: total/tier counts differ from CSV")
        if seen != set(domain_names) or not found_total:
            self.fail("README.md: domain summary table is missing catalog domains or totals")

    def published_counts(self, controls: dict, domain_names: dict):
        """Recalculate published counts from the catalog and the examples' own tags."""
        all_rows = list(controls.values())
        tally = lambda rows: [len(rows)] + [sum(r["tier"] == t for r in rows) for t in TIERS]
        baseline = [r for r in all_rows if r["scope"] != "Asset" and r["tier"] == "T1"]
        unconditional = [r for r in baseline if r["applies_to"] == "ALL"]
        conditional = [r for r in baseline if r["applies_to"] != "ALL"]
        example_count = 0
        for name in ("README.md", "guides/tiering.md", "guides/adoption.md", "CHANGELOG.md"):
            if not (self.root / name).exists():
                continue
            text = self.text(name)
            if name == "CHANGELOG.md":
                # Historical releases retain their historical totals.
                releases = list(re.finditer(r"^## \[[^\]]+\] - \d{4}-\d{2}-\d{2}\s*$", text, re.M))
                if len(releases) > 1:
                    text = text[:releases[1].start()]
            for header, rows in tables(text):
                if name == "guides/tiering.md" and header and header[0] == "Tag":
                    printed = [values[0] for _, values in rows if values]
                    if set(printed) != TAGS or len(printed) != len(TAGS):
                        self.fail(f"{name}: documented tag vocabulary differs from the supported tags")
                domain_table = header[:2] == ["#", "Domain"] and header[-4:] == ["Controls", *TIERS]
                scope_table = header == ["Scope", "Controls", *TIERS]
                if domain_table or scope_table:
                    seen = set()
                    total_seen = False
                    for number, values in rows:
                        if len(values) != len(header):
                            self.fail(f"{name}:{number}: summary table has an unexpected column count")
                            continue
                        key = values[0]
                        is_total = "Total" in values[:2]
                        if is_total:
                            chosen, total_seen = all_rows, True
                        elif domain_table:
                            chosen = [r for r in all_rows if r["domain_number"] == key]
                        else:
                            chosen = [r for r in all_rows if r["scope"] == key]
                        if not is_total:
                            if key in seen:
                                self.fail(f"{name}:{number}: duplicate summary row {key}")
                            seen.add(key)
                        if values[-4:] != [str(n) for n in tally(chosen)]:
                            self.fail(f"{name}:{number}: published domain/scope/tier counts differ from CSV")
                    expected_keys = set(domain_names) if domain_table else {r["scope"] for r in all_rows}
                    if seen != expected_keys or not total_seen:
                        self.fail(f"{name}: summary table is missing domains, scopes, or totals")
                if header and header[0] in ("Tier", "Control Tier") and header[-1] == "Controls":
                    for number, values in rows:
                        if values and values[0] in TIERS and values[-1] != str(sum(r["tier"] == values[0] for r in all_rows)):
                            self.fail(f"{name}:{number}: control-tier definition count differs from CSV")
                tag_column = next((i for i, h in enumerate(header) if h in ("Tags", "Capability tags")), None)
                if tag_column is not None and any("T1" in h or h == "Asset controls required" for h in header):
                    for number, values in rows:
                        if len(values) != len(header):
                            self.fail(f"{name}:{number}: example table has an unexpected column count")
                            continue
                        tags = {t.strip() for t in values[tag_column].split(",")}
                        if not tags or tags - (TAGS - {"ALL"}):
                            self.fail(f"{name}:{number}: example has invalid capability tags")
                            continue
                        chosen = [r for r in all_rows if r["scope"] == "Asset" and applies(r["applies_to"], tags)]
                        expected = tally(chosen)[1:]
                        if header[-1] == "Asset controls required":
                            rating = values[header.index("Rating")]
                            autonomy = values[header.index("Highest autonomy")]
                            required = {"T1"}
                            if rating in ("High", "Critical"):
                                required.add("T2")
                            if re.search(r"\bA4\b", autonomy):
                                required.add("T3")
                            reported = re.findall(r"(\d+)\s+(T[123])\b", values[-1])
                            actual = {t: int(n) for n, t in reported}
                            wanted = {t: n for t, n in zip(TIERS, expected) if t in required}
                            if actual != wanted or len(reported) != len(actual):
                                self.fail(f"{name}:{number}: risk-rated example counts differ from its tags/rating in the CSV")
                        elif values[-3:] != [str(n) for n in expected]:
                            self.fail(f"{name}:{number}: example tier counts differ from its tags in the CSV")
                        example_count += 1
            for number, line in visible_lines(text):
                plain = cell(line)
                for match in re.finditer(r"\b(\d+) controls (?:across|in) (\d+) domains\b", plain):
                    if tuple(map(int, match.groups())) != (len(controls), len(domain_names)):
                        self.fail(f"{name}:{number}: published overall control/domain count differs from CSV")
                for pattern in (r"Ballast includes (\d+) controls", r"\| (\d+) controls, (?:tiered|organized)"):
                    match = re.search(pattern, plain)
                    if match and int(match[1]) != len(controls):
                        self.fail(f"{name}:{number}: published overall count differs from CSV")
                match = re.search(r"^## The (\d+) domains$", plain)
                if match and int(match[1]) != len(domain_names):
                    self.fail(f"{name}:{number}: published domain heading count differs from CSV")
                match = re.search(r"using (\d+) tags:", plain)
                if match and int(match[1]) != len(TAGS):
                    self.fail(f"{name}:{number}: published tag count differs from supported vocabulary")
                match = re.search(r"Of the (\d+), (\d+) are implemented for each AI asset, (\d+) once by the organization's AI security program, and (\d+) once per AI vendor", plain)
                if match and tuple(map(int, match.groups())) != (len(controls), *(sum(r["scope"] == s for r in all_rows) for s in ("Asset", "Program", "Vendor"))):
                    self.fail(f"{name}:{number}: published scope summary differs from CSV")
                for match in re.finditer(r"\b(\d+) (Program|Vendor|Asset) controls\b", plain):
                    if int(match[1]) != sum(r["scope"] == match[2] for r in all_rows):
                        self.fail(f"{name}:{number}: published scope count differs from CSV")
                for match in re.finditer(r"\b(T[123]) (?:Baseline|Elevated risk|Advanced) \((\d+)(?: controls)?\)", plain):
                    if int(match[2]) != sum(r["tier"] == match[1] for r in all_rows):
                        self.fail(f"{name}:{number}: published control-tier count differs from CSV")
                for match in re.finditer(r"\b(\d+) (unconditional|conditional) (?:Program and Vendor )?(?:T1 )?controls\b", plain):
                    expected = len(unconditional if match[2] == "unconditional" else conditional)
                    if int(match[1]) != expected:
                        self.fail(f"{name}:{number}: published baseline count differs from CSV")
                match = re.search(r"\b(\d+) T1 controls for every organization, plus up to (\d+)\b", plain)
                if match and tuple(map(int, match.groups())) != (len(unconditional), len(conditional)):
                    self.fail(f"{name}:{number}: published baseline count differs from CSV")
                match = re.search(r"That is (\d+) unconditional controls \((\d+) Program, (\d+) Vendor\) and (\d+) conditional ones", plain)
                if match and tuple(map(int, match.groups())) != (len(unconditional), sum(r["scope"] == "Program" for r in unconditional), sum(r["scope"] == "Vendor" for r in unconditional), len(conditional)):
                    self.fail(f"{name}:{number}: published baseline scope breakdown differs from CSV")
                match = re.search(r"brings in (\d+) of the (\d+) conditional Program controls", plain)
                if match:
                    coding = {"CODE", "ENDPOINT", "AGENT", "ACT", "EXEC", "EXT", "UNTRUSTED"}
                    program = [r for r in conditional if r["scope"] == "Program"]
                    if tuple(map(int, match.groups())) != (sum(applies(r["applies_to"], coding) for r in program), len(program)):
                        self.fail(f"{name}:{number}: coding-agent conditional baseline differs from CSV")
                match = re.search(r"\b(\d+) baseline controls once and (\d+) asset controls for the copilot", plain)
                if match:
                    copilot = [r for r in all_rows if r["scope"] == "Asset" and applies(r["applies_to"], {"RAG", "UNTRUSTED", "MEM"})]
                    if tuple(map(int, match.groups())) != (len(unconditional), sum(r["tier"] == "T1" for r in copilot)):
                        self.fail(f"{name}:{number}: copilot baseline example differs from CSV")
                    added = re.search(r"adds its (\d+) asset T2 controls", plain)
                    if added and int(added[1]) != sum(r["tier"] == "T2" for r in copilot):
                        self.fail(f"{name}:{number}: copilot T2 example differs from CSV")
                if name == "guides/tiering.md" and re.match(r"- \d+ (?:unconditional|conditional) T1 controls", plain):
                    chosen = unconditional if "unconditional" in plain else conditional
                    ids = self.prose_ids(plain)
                    if set(ids) != {r["control_id"] for r in chosen} or len(ids) != len(set(ids)):
                        self.fail(f"{name}:{number}: listed baseline controls differ from CSV")
                match = re.search(r"The (\w+) T3 controls are (.*)", plain)
                if match:
                    ids = self.prose_ids(match[2])
                    expected_ids = {r["control_id"] for r in all_rows if r["tier"] == "T3"}
                    if self.number_word(match[1]) != len(expected_ids) or set(ids) != expected_ids or len(ids) != len(set(ids)):
                        self.fail(f"{name}:{number}: listed T3 controls/count differ from CSV")
        self.summary["example_rows"] = example_count
        if (self.root / "guides/worked-example.md").exists():
            self.worked_example(controls, unconditional)

    @staticmethod
    def prose_ids(text: str) -> list[str]:
        """Read full IDs and the shortened IDs used in control lists."""
        return ["BAL-" + n for n in re.findall(r"(?<![\w.])(?:BAL-)?(\d+\.\d+)(?![\w.])", cell(text))]

    @staticmethod
    def number_word(value: str) -> int | None:
        words = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()
        return int(value) if value.isdigit() else words.index(value.lower()) if value.lower() in words else None

    def worked_example(self, controls: dict, unconditional: list[dict]):
        name = "guides/worked-example.md"
        text = self.text(name)
        lines = [(n, cell(line)) for n, line in visible_lines(text)]
        plain = "\n".join(line for _, line in lines)
        found = re.search(r"^Tags:\s*([A-Z, ]+)\.\s*$", plain, re.M)
        if not found:
            self.fail(f"{name}: worked example needs a Tags declaration")
            return
        tags = {t.strip() for t in found[1].split(",")}
        if tags - (TAGS - {"ALL"}):
            self.fail(f"{name}: worked example has invalid capability tags")
        selected = {t: {k for k, r in controls.items() if r["scope"] == "Asset" and r["tier"] == t and applies(r["applies_to"], tags)} for t in TIERS}
        rejected = {t: {k for k, r in controls.items() if r["scope"] == "Asset" and r["tier"] == t} - selected[t] for t in TIERS}
        active, seen, listed = None, set(), {}
        for number, line in lines:
            heading = re.match(r"^### Asset (T[123])(?: controls that do not apply)?: (\d+)\b", line)
            if heading:
                tier = heading[1]
                excluded = "do not apply" in line
                active = (tier, excluded)
                seen.add(active)
                listed.setdefault(active, [])
                wanted = rejected[tier] if excluded else selected[tier]
                if int(heading[2]) != len(wanted):
                    self.fail(f"{name}:{number}: worked-example heading count differs from CSV/tags")
            elif line.startswith("#"):
                active = None
            elif active and line.startswith("|"):
                listed[active].extend(self.prose_ids(line))
            result = re.search(r"Result: (\d+) Asset rows apply to this agent, (\d+) at T1 and (\d+) at T2, out of (\d+) controls", line)
            if result and tuple(map(int, result.groups())) != (len(selected["T1"]) + len(selected["T2"]), len(selected["T1"]), len(selected["T2"]), len(controls)):
                self.fail(f"{name}:{number}: worked-example result counts differ from CSV/tags")
            baseline = re.search(r"The (\d+) unconditional Program and Vendor T1 controls", line)
            if baseline and int(baseline[1]) != len(unconditional):
                self.fail(f"{name}:{number}: worked-example baseline count differs from CSV")
            if re.search(r"asset T2 controls do not apply:", line, re.I):
                ids = self.prose_ids(line)
                count = re.search(r"(\w+) asset T2 controls do not apply:", line, re.I)
                if set(ids) != rejected["T2"] or len(ids) != len(set(ids)) or (count and self.number_word(count[1]) != len(rejected["T2"])):
                    self.fail(f"{name}:{number}: excluded T2 selection differs from CSV/tags")
        required_sections = {("T1", False), ("T1", True), ("T2", False)}
        if not required_sections <= seen:
            self.fail(f"{name}: worked-example control-selection sections are missing")
        for (tier, excluded), ids in listed.items():
            expected = rejected[tier] if excluded else selected[tier]
            if set(ids) != expected or len(ids) != len(set(ids)):
                self.fail(f"{name}: worked-example {tier} {'excluded' if excluded else 'applicable'} control selection differs from CSV/tags")

    def publication_fields(self):
        cff = self.text("CITATION.cff")
        fields = {}
        for number, line in enumerate(cff.splitlines(), 1):
            match = re.match(r"^([a-z][a-z-]*):\s*(.*)$", line)
            if match:
                key, value = match.groups()
                if key in fields:
                    self.fail(f"CITATION.cff:{number}: duplicate field {key}")
                fields[key] = value.strip().strip('"\'')
            if re.match(r"^\s*#\s*(?:date-released|repository-code):", line):
                self.fail(f"CITATION.cff:{number}: release field is still commented out")
        version = fields.get("version", "")
        if not SEMVER.fullmatch(version):
            self.fail("CITATION.cff: version must be a populated semantic release version")
        if self.tag is not None and self.tag.removeprefix("v") != version:
            self.fail(f"Release tag {self.tag} does not match CITATION.cff version {version}")
        if fields.get("cff-version") != "1.2.0":
            self.fail("CITATION.cff: cff-version must remain the supported citation schema version 1.2.0")
        released = fields.get("date-released", "")
        try:
            date.fromisoformat(released)
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", released):
                raise ValueError
        except ValueError:
            self.fail("CITATION.cff: date-released must be a valid YYYY-MM-DD date")
        repository = urlsplit(fields.get("repository-code", ""))
        if repository.scheme != "https" or repository.hostname != "github.com" or len(repository.path.strip("/").split("/")) != 2:
            self.fail("CITATION.cff: repository-code must be a populated HTTPS GitHub repository URL")
        releases = re.findall(r"^##\s+\[([^\]]+)\]\s*-\s*(\d{4}-\d{2}-\d{2})\s*$", self.text("CHANGELOG.md"), re.M)
        if not releases or releases[0] != (version, released):
            self.fail("CHANGELOG.md: first dated release must match CITATION.cff version/date")
        readme = self.text("README.md")
        if f"Version: {version}" not in readme or f"v{version}" not in readme:
            self.fail("README.md: release version badge/status does not match CITATION.cff")
        badges = re.findall(r"https://img\.shields\.io/badge/version-[^\s)\"<>]+", readme)
        badge_versions = [urlsplit(u).path.removeprefix("/badge/version-").removesuffix(".svg").rsplit("-", 1)[0] for u in badges]
        if not badges or any(v != version for v in badge_versions):
            self.fail("README.md: actual version badge URL does not match CITATION.cff")
        self.summary.update(version=version, release_date=released)

    def documents(self, controls: dict):
        md_paths = sorted(self.root.rglob("*.md"))
        for path in md_paths:
            self.text(path.relative_to(self.root).as_posix())
        for path in sorted(self.root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in (".md", ".cff", ".csv"):
                continue
            name = path.relative_to(self.root).as_posix()
            text = self.text(name)
            for number, line in visible_lines(text):
                # Inline code in contributor documentation can demonstrate scan
                # patterns and ID syntax without becoming a release placeholder.
                plain = re.sub(r"`+[^`]*`+", "", line)
                marker_source = plain if name == "CONTRIBUTING.md" or name == "docs/release-checks.md" else line
                if PUBLICATION_MARKERS.search(marker_source):
                    self.fail(f"{name}:{number}: unresolved publication placeholder")
                names = re.sub(r"https?://\S+", "", plain)
                names = names.replace("Avishkar (Avi) Nikum", "").replace("Avishkar (Avi)", "")
                if re.search(r"\bAvi(?:\s+Nikum)?\b", names):
                    self.fail(f"{name}:{number}: author name needs Avishkar (Avi) Nikum (CFF uses split name fields)")
                for key in CONTROL_ID.findall(line):
                    if key not in controls:
                        self.fail(f"{name}:{number}: unknown control ID {key}")
            if path.suffix.lower() == ".md":
                self.errors.extend(check_local_links(self.root, name, text, self.texts))
        self.summary["markdown_files"] = len(md_paths)

    def run(self):
        controls = self.catalog_and_data()
        self.publication_fields()
        self.documents(controls)
        return self.errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root (defaults to this script's parent repository)")
    parser.add_argument("--tag", help="Release tag to compare with citation metadata (for example v1.0.0)")
    args = parser.parse_args(argv)
    ref = os.environ.get("GITHUB_REF", "")
    tag = args.tag if args.tag is not None else ref.removeprefix("refs/tags/") if ref.startswith("refs/tags/") else None
    check = ReleaseCheck(args.root, tag=tag)
    errors = check.run()
    for error in errors:
        print("FAIL " + error)
    if errors:
        print(f"Release checks failed: {len(errors)} finding(s). No files changed.")
        return 1
    print(f"PASS Ballast {check.summary['version']} ({check.summary['release_date']})")
    print(f"PASS {check.summary['controls']} controls across {check.summary['domains']} domains; {check.summary['mappings']} mappings")
    print(f"PASS Control Tiers {check.summary['tiers']}; scopes {check.summary['scopes']}")
    print(f"PASS applicability grammar, published counts, {check.summary['example_rows']} example rows, and worked-example selections")
    print(f"PASS {check.summary['markdown_files']} Markdown files: local links, anchors, IDs, names, and publication placeholders")
    print("Checks are read-only. External mapping correctness, live URLs, and full CFF schema validation require separate review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
