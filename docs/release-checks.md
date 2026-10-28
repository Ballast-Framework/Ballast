# Reproducible release checks

Run the same read-only checks locally and in GitHub Actions. Python 3.10 or later
is the only requirement; the workflow uses Python 3.12. There are no runtime
packages to install and the checker makes no network requests.

From the repository root:

```powershell
python scripts/check_release.py
python -B -m unittest discover -s tests -p "test_*.py"
```

The checker also works from another directory when invoked with its full path.
Its default root is the repository containing the script. Use `--root PATH` to
check a separate working copy.

Before creating a release tag, also run `python scripts/check_release.py --tag
v1.0.0` with the intended tag. GitHub Actions checks a pushed tag automatically
against the citation version using `GITHUB_REF`.

## What the command verifies

- CSV column widths, required fields, unique control IDs, [Control Tiers](../guides/tiering.md#control-tiers), and scopes.
- Applicability expressions use the 17 documented capability tags. Commas mean
  OR and plus signs mean AND; unknown tags, empty clauses, dangling operators,
  unsupported syntax, and combinations of `ALL` with other tags fail validation.
- The complete control rows in the Markdown catalog and domain pages agree with
  `controls/control-catalog.csv`.
- Assessment-template control metadata agrees with the catalog. Intentional
  blank assessment cells and marked sample records remain allowed.
- Mapping IDs are valid, mapping keys are unique, and every control is mapped.
  Generated per-domain crosswalk tables and OWASP coverage tables agree with
  the mappings CSV; changing a valid reference also requires its tables to change.
- Published overall, domain, scope, [Control Tier](../guides/tiering.md#control-tiers) and baseline counts are
  calculated from the catalog. This includes the README, domain introductions,
  tiering and adoption guides, and the current changelog release; historical
  changelog entries retain their original counts.
- Example tables are recalculated from their printed tags and required
  [Control Tiers](../guides/tiering.md#control-tiers). The worked example's applicable and excluded control lists, headings and
  result totals are checked against the same catalog rules. A wrong control list
  fails even when its length is correct.
- Local Markdown links, images, anchors, and cited control IDs resolve.
  Linked control IDs and [Control Tier](../guides/tiering.md#control-tiers) labels are supported in tables, including
  explicit bookmarks used for GitHub-compatible links.
- Publication fields are populated, author names are consistent, and the citation,
  changelog, and README (including the actual version-badge URL) agree on release metadata. The citation schema
  version is checked separately from the release version.

It prints a concise PASS summary and returns exit code 0 on success. A failed
check prints file/line diagnostics and returns a nonzero exit code. It never
rewrites files or regenerates tables; correct the authoritative CSV and update
the corresponding documents, then rerun it. The synthetic tests deliberately
break representative fixtures to confirm those defects fail validation. They
include a misspelled tag repeated consistently across source files, invalid
AND/OR expressions, stale counts after a [Control Tier](../guides/tiering.md#control-tiers) change, and incorrect example
control selections.

These checks verify the published examples against their stated tags and risk
ratings. A reviewer still needs to decide whether those tags and ratings describe
the asset correctly, whether policy requirements are sound, and whether a baseline
control depends on a higher [Control Tier](../guides/tiering.md#control-tiers). Automated checks do not make those
security judgments.

## Maintaining internal links

Use repository-relative Markdown links to the control catalog's stable control
bookmarks, such as [BAL-1.13](../controls/control-catalog.md#bal-1-13).
The tiering guide defines bookmarks for each [Control Tier](../guides/tiering.md#control-tiers)
and [autonomy level](../guides/tiering.md#autonomy-levels). Preserve these bookmarks
when editing their tables so existing links continue to work on GitHub.
CSV identifiers, field names and enumerated values remain plain text for filtering
and automated processing; the Markdown documents provide the clickable references.

## Release procedure

1. Update the catalog or mappings in their CSV source of truth, then synchronize
   the Markdown tables and assessment template.
2. Update the release version and ISO-format release date in `CITATION.cff` and
   `CHANGELOG.md`, and the version badge/status in `README.md`.
3. Run both commands above and review the complete diff.
4. Review external source editions, mappings, references, reporting contacts,
   and any presentation distributed with the release. Automated checks cannot
   decide whether a control or mapping is substantively correct.
5. When publishing is authorized, push the reviewed changes. The same commands
   run on pushes, pull requests, and manually dispatched workflow runs. Require
   the `validate` job in branch protection if maintainers want it enforced.
6. After checks pass, create the matching version tag and GitHub Release. The
   checker validates file metadata; it does not create a tag, publish a release,
   change repository visibility, or upload anything.

Full CFF schema validation is a separate optional check. In a dedicated Python
environment, install `cffconvert` and run `cffconvert --validate`; pin the chosen
dependency version in that environment if it becomes part of required CI. The
stdlib checker validates the release fields but does not claim full YAML/CFF
schema validation. Live external-URL availability is also a separate check.
