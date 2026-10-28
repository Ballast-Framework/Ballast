# Changelog

Notable modifications to the Ballast AI Security Framework are documented herein. The structure adheres to [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Version identifiers conform to [versioning policy](CONTRIBUTING.md#versioning), which delineates major, minor, and patch releases based on their impact on conformance assertions.

## [1.0.0] - 2026-10-25

Initial public release. Ballast is practitioner-authored and has not yet been independently validated; feedback is welcome. What this release does not yet cover is listed in [KNOWN-GAPS.md](KNOWN-GAPS.md).

### Added

- An optional [AISMM-based Excel maturity scorecard](guides/maturity/README.md) for program-level self-assessment, with blank inputs, scores validated as integers from 1 to 5, and summaries calculated only from complete, valid ratings. The overall average gives each category equal weight. Identifying metadata and unused external workbook references have been removed from the Ballast copy.
- **Reproducible release checks:** a read-only Python validator, synthetic defect tests and a GitHub Actions workflow. See the [release-check guide](docs/release-checks.md).
- **Tri-Sphere graphic** in the README, linking principles, controls and maturity.

- **128 controls in 8 domains**, each with a requirement, [Control Tier](guides/tiering.md#control-tiers), scope, applies_to expression, evidence examples and implementation notes, in `controls/control-catalog.csv` (the source of truth) and `controls/control-catalog.md`, with one page per domain under `framework/domains/`:

| # | Domain | Controls | [T1](guides/tiering.md#t1) | [T2](guides/tiering.md#t2) | [T3](guides/tiering.md#t3) |
|---|---|---|---|---|---|
| 1 | AI Governance, Inventory & Classification | 15 | 14 | 1 | 0 |
| 2 | Agent Identity, Authentication & Lifecycle | 13 | 8 | 4 | 1 |
| 3 | Delegated Authorization & Least Agency | 13 | 8 | 5 | 0 |
| 4 | Data Security, Provenance & Trust | 16 | 9 | 6 | 1 |
| 5 | Secure AI SDLC & Supply Chain | 23 | 16 | 7 | 0 |
| 6 | Runtime Guardrails & Containment | 22 | 13 | 8 | 1 |
| 7 | Observability, Detection & Response | 13 | 4 | 8 | 1 |
| 8 | Third-Party, Vendor & Shadow AI Risk | 13 | 11 | 2 | 0 |
| | **Total** | **128** | **83** | **41** | **4** |

- **Three [Control Tiers](guides/tiering.md#control-tiers):** [T1](guides/tiering.md#t1) Baseline (83 controls), [T2](guides/tiering.md#t2) Elevated risk (41) and [T3](guides/tiering.md#t3) Advanced (4). No [T1](guides/tiering.md#t1) control depends on a [T2](guides/tiering.md#t2) or [T3](guides/tiering.md#t3) control.
- **Scope on every control:** 37 Program controls, implemented once by the organization's AI security program and inherited by every asset; 5 Vendor controls, assessed once per AI vendor, service and plan; and 86 Asset controls, implemented and evidenced for each in-scope AI asset or inherited from a shared platform.
- **Capability tags** in the applies_to column, using 17 tags: ALL, BUILT, AGENT, ACT, AUTO, EXEC, RAG, MEM, UNTRUSTED, EXT, MULTI, MODEL, INFRA, CODE, ENDPOINT, PUBLIC and LOWCODE. A comma means OR and a plus sign means AND. "Not applicable" is derived from an asset's tags and is never chosen ad hoc.
- **Asset risk rating ([BAL-1.5](controls/control-catalog.md#bal-1-5)):** each AI asset is rated Low, Medium, High or Critical using rules TR-A to TR-D (restricted data, [autonomy](guides/tiering.md#autonomy-levels) or execution, untrusted-input combination or external users, and consequential use). [T1](guides/tiering.md#t1) applies to every in-scope asset, pilots and developer tools on real data included; [T2](guides/tiering.md#t2) applies to assets rated High or Critical; [T3](guides/tiering.md#t3) is required for any asset with an action class at [A4](guides/tiering.md#a4) and recommended for Critical assets.
- **[Autonomy levels](guides/tiering.md#autonomy-levels) [A0](guides/tiering.md#a0)-[A4](guides/tiering.md#a4)** (Read-only, Suggest, Act with approval, Bounded autonomous, [High autonomy](guides/tiering.md#autonomy-levels)), recorded per action class with the initiation mode and enforced outside the model ([BAL-3.1](controls/control-catalog.md#bal-3-1)). Raising an action class, or deploying an agent with any action class above [A2](guides/tiering.md#a2), requires recorded evidence and sign-off at a promotion gate. [A4](guides/tiering.md#a4) requires a time-bound [A4](guides/tiering.md#a4) authorization and is prohibited for consequential decisions about individuals, restricted data, irreversible financial actions and assets that do not meet [BAL-3.5](controls/control-catalog.md#bal-3-5).
- **Eight core principles** in `framework/principles.md`, each listing the controls that implement it, with the two directions of agent security: protect our agents from the world, and protect ourselves from our agents.
- **Control-level mappings** in `mappings/control-mappings.csv`, one row per control and reference, to the [OWASP Top 10 for LLM Applications 2026](https://github.com/GenAI-Security-Project/GenAI-LLM-Top10/blob/main/2026/README.md), the [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), [MITRE ATLAS](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.09) (data release 2026.09), [NIST AI RMF 1.0](https://doi.org/10.6028/NIST.AI.100-1) and [ISO/IEC 42001:2023](https://www.iso.org/standard/42001) Annex A. `mappings/crosswalk.md` adds per-domain tables generated from the CSV, coverage tables for both OWASP lists, a framework versions line, a sources and terms table, a category-level alignment with the [CSA AI Security Maturity Model (AISMM)](https://cloudsecurityalliance.org/artifacts/ai-security-maturity-model), informative references that are not mapped, and a watch list.
- **Guides:** `guides/tiering.md` (tags, scope, [Control Tiers](guides/tiering.md#control-tiers), [autonomy levels](guides/tiering.md#autonomy-levels), the risk rating rubric, the program baseline, the pilot minimum, non-acceptable controls, and exceptions and risk acceptance), `guides/adoption.md` (adoption path, assessment procedure, evidence and counting rules, metrics and conformance claims) and `guides/worked-example.md` (one agent assessed end to end).
- **Templates:** `guides/assessment-template.csv`, `guides/asset-register-template.csv` and `guides/exceptions-log-template.csv`, with illustrative example rows.
- **Glossary** of defined terms in `framework/glossary.md`.
- **Known gaps and roadmap** in `KNOWN-GAPS.md`.
- **Governance files:** `CONTRIBUTING.md` (writing rules for controls, the control ID policy, versioning by effect on conformance claims, governance and a release checklist), `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CITATION.cff` and the CC BY 4.0 `LICENSE`.
