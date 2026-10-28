# Contributing to the Ballast AI Security Framework

Ballast improves through practitioner feedback. Contributions of all sizes are welcome, from a wording fix to a new control. Version 1.0.0 is the first public release and has not yet been independently validated, so reports on unclear, untestable or missing controls are especially useful now. [KNOWN-GAPS.md](KNOWN-GAPS.md) lists what v1.0 does not yet cover.

Participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Report anything sensitive, such as guidance that could cause harm if followed, privately as described in [SECURITY.md](SECURITY.md) rather than in a public issue.

## Ways to contribute

- **Report an issue:** unclear wording, a control two assessors would judge differently, a gap in coverage, an incorrect mapping, or a broken link.
- **Propose a control or a change to one:** open an issue first so the proposal can be discussed before a pull request.
- **Improve mappings:** corrections or additions to `mappings/control-mappings.csv`, citing the framework version and linking to the source publication.
- **Share pilot results:** what was infeasible, ambiguous or missing when you assessed an AI asset against Ballast (anonymized is fine).

## Proposing a new or changed control

Open an issue that includes:

1. **Domain:** which of the 8 domains it belongs to.
2. **Control name:** a short title.
3. **Requirement:** one to four sentences describing the outcome, following the [writing rules](#writing-rules-for-controls).
4. **Proposed [Control Tier](guides/tiering.md#control-tiers):** [T1](guides/tiering.md#t1), [T2](guides/tiering.md#t2) or [T3](guides/tiering.md#t3), with a short rationale against the [Control Tier](guides/tiering.md#control-tiers) definitions. [T1](guides/tiering.md#t1) is the baseline for every in-scope asset carrying the control's tags; [T2](guides/tiering.md#t2) applies to assets rated High or Critical under [BAL-1.5](controls/control-catalog.md#bal-1-5); [T3](guides/tiering.md#t3) is required for assets with an action class at [autonomy level](guides/tiering.md#autonomy-levels) [A4](guides/tiering.md#a4).
5. **Scope:** Program (implemented once by the AI security program), Vendor (assessed once per AI vendor, service and plan) or Asset (implemented for each in-scope AI asset).
6. **applies_to tags:** the capability tags that make the control applicable, from the vocabulary in the [tiering guide](guides/tiering.md): ALL, BUILT, AGENT, ACT, AUTO, EXEC, RAG, MEM, UNTRUSTED, EXT, MULTI, MODEL, INFRA, CODE, ENDPOINT, PUBLIC, LOWCODE. A comma means OR and a plus sign means AND.
7. **Risk addressed:** the threat or failure mode, with identifiers where they apply: [OWASP Top 10 for LLM Applications 2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/README.md) (for example LLM01:2026), [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) (for example ASI02) and [MITRE ATLAS](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.09) techniques (for example AML.T0051, stating the ATLAS release). Add an incident report or research paper if one exists.
8. **Overlap check:** existing controls that are related, why they do not already cover the risk, and any existing control the proposal would change.
9. **Evidence examples:** two or three concrete items an assessor could request.

For a change to an existing control, give its ID, the proposed wording, and which kind of change it is under [Versioning](#versioning).

## Writing rules for controls

1. **One control objective.** Enumerated sub-requirements are allowed; the control is implemented only when all of them are met.
2. **Outcome, not product.** A control must be satisfiable by process plus any tool. Requirements name no vendors or products. Standards may be given as examples, for example "OAuth token exchange ([RFC 8693](https://www.rfc-editor.org/info/rfc8693/))".
3. **AI-specific delta only.** If a control touches general IT hygiene, state only what AI changes: a new asset type, data flow or failure mode.
4. **Testable.** Two assessors should reach the same pass or fail result from the same evidence.
5. **Parameters.** Where a number is needed, write "defined" with an organization-defined parameter (for example "within a defined period"), and suggest a default in the evidence examples or guidance (for example "15 minutes").
6. **No absolute promises.** Do not write that a model will "never" do something, "cannot" do it, or is "prevented" from doing it unless the outcome is enforced deterministically outside the model.
7. **Global definitions.** "Detected" means an alert reaches an accountable owner and is handled under a defined response. The definition applies everywhere, so do not restate it in each control.
8. **Plain English.** Complete sentences in the present tense, one to four sentences, up to about 90 words; a control with enumerated sub-requirements may run to about 160 words.
9. **Dependencies.** A [T1](guides/tiering.md#t1) control must not depend on a [T2](guides/tiering.md#t2) or [T3](guides/tiering.md#t3) control. Cross-references use current control IDs.
10. **Evidence examples.** Two or three concrete items an assessor can request, separated by semicolons, about 25 to 45 words in total.

## Third-party text and sources

- **Do not paste text from OWASP publications.** They are licensed under CC BY-SA 4.0, whose ShareAlike terms are incompatible with Ballast's CC BY 4.0 license.
- **Do not paste text from ISO/IEC or other paywalled standards**, or from sources whose terms do not permit redistribution, such as CSA publications.
- **Reference identifiers only**, with a short paraphrased label and a link to the source, for example "LLM01:2026 Prompt Injection", "ASI03" or "[ISO/IEC 42001](https://www.iso.org/standard/42001) A.6.2.6". Paraphrase even permissively licensed sources such as NIST publications and [MITRE ATLAS](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.09) data, and state the version you used.

## Control ID policy

- IDs follow `BAL-<domain>.<n>`.
- The register is append-only. New controls are added at the end of their domain. A withdrawn control keeps its ID and is marked as withdrawn with the reason and any replacing control. IDs are never reused or reassigned.
- An ID never takes on a different objective. Tightening or relaxing a control's requirement keeps its ID and is versioned as below. Replacing its objective, or moving it to another domain, withdraws the ID and adds a new one.

## Versioning

Version numbers are defined by their effect on conformance claims. A conformance claim names the exact version it was made against, for example "self-assessed against Ballast v1.0.0, [T1](guides/tiering.md#t1) scope".

- **Major** (for example 2.0.0): removes or withdraws a control, changes a control's objective, moves it to another domain, tightens an existing requirement or makes it apply to more assets, such as moving a control from [T2](guides/tiering.md#t2) to [T1](guides/tiering.md#t1).
- **Minor** (for example 1.1.0): additive changes. These include new controls at any [Control Tier](guides/tiering.md#control-tiers), each with a stated adoption grace period (for example 6 months) during which a claim against the new version may record the new control as planned; relaxed requirements or narrower applicability, such as moving a control from [T1](guides/tiering.md#t1) to [T2](guides/tiering.md#t2); mapping updates, including new frameworks, new framework versions and corrected references; applies_to clarifications that do not bring more assets into scope; and new guidance, templates or evidence examples.
- **Patch** (for example 1.0.1): editorial changes only, such as wording, typos, formatting and links, with no change to any requirement, [Control Tier](guides/tiering.md#control-tiers), scope, applies_to value or mapping.

Every release is recorded in [CHANGELOG.md](CHANGELOG.md).

## Governance

- **Maintainers.** Ballast is maintained by its authors, Raoul Hira (lead) and Avishkar (Avi) Nikum. Adding independent maintainers, a named reviewer list and a possible neutral home for the project are on the [roadmap](KNOWN-GAPS.md#project-governance).
- **How decisions are made.** Changes to controls, [Control Tiers](guides/tiering.md#control-tiers), scope, applies_to values or mappings are proposed in an issue and stay open for comment for an issue period, normally at least 14 days, before the maintainers decide; where they disagree, the lead maintainer decides. The decision and its rationale are recorded on the issue. Editorial fixes may be merged without a waiting period.
- **Vendor affiliation.** Contributors who work for, advise or hold a material interest in a vendor of AI or AI security products or services disclose that affiliation in the issue or pull request. No control may require or favor a specific product.
- **Mapping reviews.** Mappings are reviewed when a referenced framework publishes a new version and at least once a year. [MITRE ATLAS](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.09) publishes frequently, so the ATLAS release is re-validated before each Ballast release.

## Release checklist

Before tagging a release, run `python scripts/check_release.py` from the repository root. The checks require Python 3.10 or later and use only the standard library. See [Reproducible release checks](docs/release-checks.md) for commands, coverage and the remaining human checks.

The same command runs in GitHub Actions after the workflow is uploaded. It checks the current files without changing them.

Before tagging a release:

1. **Counts regenerated from the CSV.** Recompute totals, domain, [Control Tier](guides/tiering.md#control-tiers) and scope counts, per-asset-type counts and the program baseline from `controls/control-catalog.csv`, and update every document that states them.
2. **IDs checked.** Every BAL ID cited in the documents and any accompanying presentation materials exists in the catalog, and no [T1](guides/tiering.md#t1) control depends on a [T2](guides/tiering.md#t2) or [T3](guides/tiering.md#t3) control.
3. **Mappings regenerated.** The crosswalk tables are regenerated from `mappings/control-mappings.csv`, and the framework versions line names the releases actually checked.
4. **Placeholder scan.** Search all `.md`, `.cff` and `.csv` files, and, if a presentation accompanies the release, its text and file metadata, for unfilled placeholders and leftover to-do comments, for example with the pattern `\[(AUTHOR|PRESENTER|RELEASE|REPOSITORY|GITHUB|QR|SECURITY|CONDUCT|DISCLOSURE)[^]]*\]`. Nothing may remain.
5. **CITATION.cff.** The version matches the release tag, `date-released` and `repository-code` are filled in and uncommented, and the file validates (for example with `cffconvert --validate`).
6. **Deck sync.** If a presentation accompanies the release, every control ID, count, [Control Tier](guides/tiering.md#control-tiers) definition and URL in it matches the tagged release.
7. **Changelog.** The release entry is complete and dated, and lists any withdrawn IDs.

## Licensing of contributions

By contributing, you agree that your contributions are licensed under [CC BY 4.0](LICENSE), the same license as the rest of Ballast. By submitting, you confirm that you have the right to license your contribution under CC BY 4.0, including any permission your employer requires.
