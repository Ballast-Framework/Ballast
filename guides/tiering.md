# Control Tiers and Applicability

Ballast includes 128 controls; however, no organization enforces all of these controls for each AI asset. This guide details how to determine which controls are applicable to your organization and to each AI asset, how an asset's risk rating influences which [Control Tiers](#control-tiers) are necessary, and how exceptions function. Defined terms such as AI asset, agent, untrusted content, [autonomy level](#autonomy-levels), and others are listed in the [glossary](../framework/glossary.md).

## How Ballast decides which controls apply

Three steps, in this order:

1. **Tags: does the control apply at all?** Every control has an applies-to expression built from capability tags. Each AI asset records its tags with its risk rating ([BAL-1.5](../controls/control-catalog.md#bal-1-5)). A control applies to the asset when the asset's tags satisfy the expression. If they do not, the control is Not applicable. That result is derived from the tags; nobody chooses it.
2. **Scope: where is the control implemented and assessed?** Program controls are implemented once by the organization, Vendor controls once per AI vendor, service and plan, and Asset controls for each AI asset (or once by a shared platform the asset inherits from).
3. **[Control Tier](#control-tiers): is the control required now?** [T1](#t1) controls are required for every in-scope asset. [T2](#t2) controls are added when the asset is rated High or Critical. [T3](#t3) controls are added when any of the asset's action classes runs at [autonomy level](#autonomy-levels) [A4](#a4).

An asset's required control set is therefore: the Asset controls whose tags it carries, at the [Control Tiers](#control-tiers) its rating requires, plus the Program and Vendor controls it inherits. Record tags and ratings in the [asset register template](asset-register-template.csv); the [control catalog](../controls/control-catalog.csv) holds each control's [Control Tier](#control-tiers), scope and applies-to expression.

## Scope

| Scope | Implemented and assessed | Controls | When it is required |
|---|---|---|---|
| Program | Once, by the organization's AI security program. Every AI asset inherits it. | 37 | Program [T1](#t1): every organization that uses AI, subject to the control's tags. Program [T2](#t2): once the inventory holds any High or Critical asset that carries the control's tags. Program [T3](#t3): once any asset has an action class at [A4](#a4). |
| Vendor | Once per AI vendor, service and plan. Every asset that uses that service inherits it. | 5 | Vendor [T1](#t1): every AI vendor service in use. Vendor [T2](#t2): once a High or Critical asset that carries the control's tags uses the service. |
| Asset | For each in-scope AI asset. | 86 | By the asset's tags and risk rating, as described below. |

For Program and Vendor controls, a tag within the applies-to expression signifies 'required when any in-scope asset possesses this tag'. For instance, [BAL-1.9](../controls/control-catalog.md#bal-1-9) (Endpoint AI discovery) is mandated once the organization possesses any asset marked ENDPOINT. Count instances of unsanctioned utilization identified through discovery ([BAL-1.9](../controls/control-catalog.md#bal-1-9), [BAL-8.9](../controls/control-catalog.md#bal-8-9)) when assessing whether a tag is present: an organization where developers employ unsanctioned coding agents will have CODE assets.

**Inheritance from platforms.** An organization-wide platform, such as an AI gateway, an agent-building platform, a managed coding-agent configuration or a copilot tenant baseline, can implement an Asset control once for every asset onboarded to it. Each asset names the provider in inherited_from and links to the shared assessment and current evidence showing it is covered. Assess the shared control once. A gap or stale evidence in a platform, Program or Vendor control is a gap for dependent assets. Any tailoring or risk acceptance must explicitly cover those assets and their risk ratings. Count each asset's required control once, without adding shared-evidence records to asset counts or coverage totals.

## Applies-to tags

| Tag | Applies when the asset... |
|---|---|
| ALL | is any AI asset (for Program and Vendor scope: any organization, or any AI vendor) |
| BUILT | is built or configured by the organization: custom applications and agents, low-code agents, configured prompts, tools or retrieval. Vendor-operated SaaS AI features are not BUILT. |
| AGENT | can call tools, functions, connectors or APIs |
| ACT | can change state or communicate externally: any action class at [A2](#a2) or above |
| AUTO | acts without per-action human approval for some action class: [A3](#a3) or above |
| EXEC | executes code or shell commands, or performs model-directed filesystem writes; see the controlled-export rule below |
| RAG | retrieves or grounds on enterprise content, including vendor copilots that ground on users' permissions |
| MEM | has persistent memory across sessions |
| UNTRUSTED | processes content not authored by the organization or the invoking user: email, web pages, shared or uploaded files, tickets, tool or MCP output, other agents. A run triggered by external content counts as UNTRUSTED. |
| EXT | uses MCP servers, plugins, skills, connectors or extensions |
| MULTI | invokes, or is invoked by, other agents |
| MODEL | involves model weights the organization hosts, fine-tunes, trains or ingests |
| INFRA | involves self-hosted AI services the organization operates: inference servers, AI gateways, agent or workflow builders, MCP servers, vector databases, notebooks or ML control planes |
| CODE | is an AI coding assistant or coding agent, or the code one produces |
| ENDPOINT | runs on managed endpoints: desktop agents, CLIs, IDE and browser extensions, local model runtimes |
| PUBLIC | has users outside the organization |
| LOWCODE | is a low-code or end-user agent builder the organization offers |

**Reading an expression.** A comma means OR and a plus sign means AND. [BAL-5.4](../controls/control-catalog.md#bal-5-4) (BUILT+UNTRUSTED) applies only to an asset that is both built by the organization and processes untrusted content. [BAL-6.10](../controls/control-catalog.md#bal-6-10) (EXEC, BUILT+AGENT) applies to any asset tagged EXEC, and to any agent the organization builds.

**Controlled exports.** EXEC covers code, shell commands and model-directed filesystem writes. A data-only export through an application that controls the destination, format and recipient permissions does not add EXEC by itself, provided it cannot write executable content or configuration files. The export remains a state-changing action. Ordinary file reads alone do not add EXEC.

**Tagging rules.**

- Tag what the asset can do as deployed (features enabled, permissions granted, tools and connectors attached), not what it is usually asked to do.
- Tags are part of the [BAL-1.5](../controls/control-catalog.md#bal-1-5) capability profile. Adding a tag is a material change, which re-opens registration ([BAL-1.6](../controls/control-catalog.md#bal-1-6)) and re-derives applicability.
- Not applicable comes only from tags. An assessor who believes a tagged control should not apply uses tailoring or risk acceptance (see [Exceptions](#exceptions-and-risk-acceptance)), not Not applicable.
- A missing prerequisite is a gap, not Not applicable. For example, an organization with no sensitivity-labeling scheme has a gap against [BAL-4.1](../controls/control-catalog.md#bal-4-1).
- A control whose enforcement point sits inside a vendor's service is not Not applicable either (see [Vendor-operated assets](#vendor-operated-assets)).
- **Conditional requirements.** Some controls apply by tag but state a condition in their text, for example [BAL-3.13](../controls/control-catalog.md#bal-3-13) (financial, permission-grant and irreversible production classes), [BAL-5.23](../controls/control-catalog.md#bal-5-23) (agents in CI/CD or repository automation), [BAL-2.8](../controls/control-catalog.md#bal-2-8) (an INFRA asset that operates no MCP server), [BAL-6.8](../controls/control-catalog.md#bal-6-8) (user-facing output), [BAL-8.6](../controls/control-catalog.md#bal-8-6) (the vendor operates the runtime, tools, outbound requests or rendering) and [BAL-8.13](../controls/control-catalog.md#bal-8-13) (business-critical processes). Where the condition does not arise, record Implemented with evidence that it is absent, not Not applicable.
- **MODEL artifacts.** [BAL-5.12](../controls/control-catalog.md#bal-5-12) to [5.14](../controls/control-catalog.md#bal-5-14) act on weight, adapter, tokenizer and template artifacts the organization holds. An organization that fine-tunes only through a provider API holds none and records them under the conditional rule; [BAL-4.13](../controls/control-catalog.md#bal-4-13), [4.15](../controls/control-catalog.md#bal-4-15) and [5.15](../controls/control-catalog.md#bal-5-15) still apply.
- **Repository automation.** An agent that runs in CI/CD or repository automation, or acts on repositories, issues or pull requests, carries CODE.
- **Hosting model.** Record whether the asset is organization-operated, vendor-operated or built on a vendor platform ([BAL-1.5](../controls/control-catalog.md#bal-1-5)). This selects the evidence route for vendor-operated enforcement points and shows whether [BAL-8.6](../controls/control-catalog.md#bal-8-6)'s condition arises.

<a id="tiers"></a>

## Control Tiers

| [Control Tier](#control-tiers) | Name | Required for | Controls |
|---|---|---|---|
| <a id="t1"></a>[T1](#t1) | Baseline | Every in-scope AI asset, for the [T1](#t1) controls whose tags it carries, and every organization (Program [T1](#t1)) | 83 |
| <a id="t2"></a>[T2](#t2) | Elevated risk | Assets rated High or Critical under [BAL-1.5](../controls/control-catalog.md#bal-1-5). Program [T2](#t2) controls once the inventory holds any High or Critical asset that carries the control's tags. | 41 |
| <a id="t3"></a>[T3](#t3) | Advanced | Any asset with an action class at [autonomy level](#autonomy-levels) [A4](#a4). Recommended for Critical assets; optional additional protection otherwise. | 4 |

[Control Tiers](#control-tiers) are cumulative: a High asset meets its [T1](#t1) and [T2](#t2) controls. No [T1](#t1) control depends on a [T2](#t2) or [T3](#t3) control. The four [T3](#t3) controls are [BAL-2.13](../controls/control-catalog.md#bal-2-13) (sender-constrained agent tokens), [BAL-4.16](../controls/control-catalog.md#bal-4-16) (embedding-space attack detection), [BAL-6.22](../controls/control-catalog.md#bal-6-22) (provenance-tracked execution) and [BAL-7.13](../controls/control-catalog.md#bal-7-13) (AI honeypots and canary tokens).

**What is in scope.** Every AI asset in production, and every pilot or developer tool that touches real (non-synthetic) organizational data, users, identities or credentials. Pilots start from the [pilot minimum](#pilot-minimum) below. A sandbox that uses only synthetic data, with no real identities, credentials or users, is outside [Control Tier](#control-tiers) scope; registering it before its first real use ([BAL-1.6](../controls/control-catalog.md#bal-1-6)) brings it in.

**Terminology.** "[Control Tier](#control-tiers)" means a [Control Tier](#control-tiers) only. An asset has a risk rating (Low, Medium, High, Critical), and a vendor offering has a plan or edition.

## Autonomy levels

[Autonomy](#autonomy-levels) is recorded per action class, with the initiation mode (human-initiated or event-triggered), and enforced under [BAL-3.1](../controls/control-catalog.md#bal-3-1). An asset's agency is the highest level across its action classes. Full definitions are in [Domain 3](../framework/domains/03-delegated-authorization-and-least-agency.md).

| Level | Name | Meaning |
|---|---|---|
| <a id="a0"></a>[A0](#a0) | Read-only | No state-changing tools. Rendering links or images, fetching URLs and writing memory are still outbound channels ([BAL-3.5](../controls/control-catalog.md#bal-3-5), [BAL-6.3](../controls/control-catalog.md#bal-6-3)). |
| <a id="a1"></a>[A1](#a1) | Suggest | Proposes content or actions that a human carries out through a separate, normal channel. One-click execution of a proposed tool call is [A2](#a2). |
| <a id="a2"></a>[A2](#a2) | Act with approval | Executes after per-action human approval rendered by the enforcement point ([BAL-3.6](../controls/control-catalog.md#bal-3-6)). If auto-approve is enabled for an action class, that class is [A3](#a3). |
| <a id="a3"></a>[A3](#a3) | Bounded autonomous | Acts without per-action approval inside a declared envelope of tools, scopes, egress, rate, budget and time. [BAL-3.6](../controls/control-catalog.md#bal-3-6) high-risk classes need per-action approval unless an authorized person approves specified actions and targets within recorded limits and an expiry date at the promotion gate. Limits are enforced outside the model; other required reviews still apply. |
| <a id="a4"></a>[A4](#a4) | [High autonomy](#autonomy-levels) | Self-initiated or open-ended goals. Allowed only with an [A4](#a4) authorization ([BAL-1.13](../controls/control-catalog.md#bal-1-13)), approved by an executive risk owner, with all applicable [T2](#t2) and [T3](#t3) controls implemented and [BAL-3.7](../controls/control-catalog.md#bal-3-7) tested. Prohibited in the cases listed under [Non-acceptable controls](#non-acceptable-controls). |

Raising an action class, or deploying an agent with any action class above [A2](#a2), requires evidence at a promotion gate ([BAL-3.1](../controls/control-catalog.md#bal-3-1)). An agent identity cannot change its own level, tools, scopes or approval settings, or create agents, triggers or schedules at a higher level than its own. A scheduled task limited to ordinary reads remains [A0](#a0). Choosing its own goals or starting work without a human-defined task remains subject to [A4](#a4). Secret retrieval, privileged credential use and outbound actions keep their existing approval requirements.

## Asset risk rating rubric

[BAL-1.5](../controls/control-catalog.md#bal-1-5) rates every AI asset on five inputs: **reach** (who uses it and how widely), **exposure** (untrusted input and external users), **access** (the most sensitive data and systems it can reach), **agency** (the highest [autonomy level](#autonomy-levels) across its action classes) and **consequential use**.

An asset is **High** if any of the following is true:

- **TR-A Restricted data.** It can reach restricted or regulated data as defined by the organization's classification scheme, for example health data, payment card data, special-category personal data, credentials and secrets, or privileged systems. Reaching internal or client-confidential data alone does not meet TR-A.
- **TR-B [Autonomy](#autonomy-levels) or execution.** Any action class is at [A3](#a3) or above, or the asset carries the EXEC tag.
- **TR-C Untrusted-input combination or external users.** In one session it holds all three [BAL-3.5](../controls/control-catalog.md#bal-3-5) properties: untrusted input, access to sensitive data or systems, and a channel that changes state or communicates externally, including rendering links or images. Or it has external users (PUBLIC).
- **TR-D Consequential use.** It makes or materially supports consequential decisions about individuals, or is classified as high-risk under applicable AI law ([BAL-1.12](../controls/control-catalog.md#bal-1-12)).

An asset is **Critical** if any action class is at [A4](#a4), or if TR-D applies together with TR-B or TR-C.

Otherwise the asset is **Low or Medium**. The organization defines the split between the two; both require [T1](#t1) only. Factors that do not meet a rule, such as reach, the number of tools or persistent memory, still inform the Low or Medium split, the approval workflow and the review cadence.

TR-C is judged on what the asset holds, not on how well it is constrained. An asset that drops one of the three properties (for example by splitting the workflow so no session holds all three) does not meet TR-C. An asset that keeps all three and constrains each outbound action under [BAL-3.5](../controls/control-catalog.md#bal-3-5) still meets TR-C: those constraints are what make it acceptable to run as a High asset.

| Risk rating | [Control Tiers](#control-tiers) required |
|---|---|
| Low or Medium | [T1](#t1) |
| High | [T1](#t1) + [T2](#t2) |
| Critical | [T1](#t1) + [T2](#t2), with [T3](#t3) recommended; [T3](#t3) required where any action class is at [A4](#a4) |

The rating also establishes the approval workflow at intake ([BAL-1.6](../controls/control-catalog.md#bal-1-6)), the requisite authority to approve exceptions ([BAL-1.13](../controls/control-catalog.md#bal-1-13)), the frequency of access certification for agent identities ([BAL-2.2](../controls/control-catalog.md#bal-2-2)), the upper limit of credential lifetimes ([BAL-2.4](../controls/control-catalog.md#bal-2-4)), the process for grant recertification ([BAL-2.7](../controls/control-catalog.md#bal-2-7)), and the review frequency. The asset undergoes re-rating following every significant change.

### Worked examples

Control counts are Asset-scope controls for an asset with exactly the tags shown. Program and Vendor controls are inherited and not counted here.

| Asset | Tags | Highest [autonomy](#autonomy-levels) | Rules met | Rating | Asset controls required |
|---|---|---|---|---|---|
| Embedded SaaS copilot that reads email: vendor-operated, grounds on the user's mailbox and files, drafts replies the user sends, memory on | RAG, UNTRUSTED, MEM | [A1](#a1) | TR-C: inbound email is untrusted, the mailbox and files are sensitive, and rendered links and images are an outbound channel | High | 15 [T1](#t1) + 3 [T2](#t2) |
| Internal RAG assistant over HR policies: built in-house, answers employees' questions from policy documents written by HR, no tools | BUILT, RAG | [A0](#a0) | None: the content is authored by the organization, it holds no restricted data and it has no external users | Low or Medium | 21 [T1](#t1) |
| AI coding agent on developer endpoints: edits files, runs commands and tests, uses MCP servers, reads repositories, issues and web pages | CODE, ENDPOINT, AGENT, ACT, EXEC, EXT, UNTRUSTED | [A2](#a2) (auto-approve modes are disabled on managed endpoints by [BAL-6.16](../controls/control-catalog.md#bal-6-16); [A3](#a3) only in approved disposable sandboxes) | TR-B (EXEC); TR-C (untrusted issues and web content, access to source code, outbound network and repository writes) | High | 28 [T1](#t1) + 9 [T2](#t2) |
| Claims-intake email agent: triggered by inbound email, extracts claimant details including health information, uses two internal MCP servers, writes draft claim records that an adjuster approves one by one | BUILT, AGENT, ACT, UNTRUSTED, EXT | [A2](#a2) | TR-A (regulated health and personal data); TR-C (untrusted email, claimant data, record writes) | High | 39 [T1](#t1) + 20 [T2](#t2) |
| Autonomous IT-operations agent: triggered by alerts and tickets, restarts services, runs remediation scripts and changes configuration within a declared envelope, uses ITSM and cloud connectors | BUILT, AGENT, ACT, AUTO, EXEC, EXT, UNTRUSTED | [A3](#a3) | TR-A (privileged systems); TR-B ([A3](#a3), EXEC); TR-C (ticket and log content an attacker can influence, privileged access, state changes) | High | 40 [T1](#t1) + 24 [T2](#t2) |

Notes on the examples:

- **SaaS copilot.** Removing email from grounding, or switching off rendering of external links and images, removes a TR-C property. If the mailboxes hold restricted data, TR-A applies as well.
- **HR assistant.** Adding employee case files or medical-leave records to the index meets TR-A and makes the assistant High.
- **Coding agent.** It also brings in 9 of the 10 conditional Program controls (those tagged CODE, ENDPOINT or EXT).
- **Claims-intake agent.** Extracting and routing claim details is not a consequential decision. If the agent scored claims, flagged fraud or recommended outcomes that adjusters rely on, TR-D would apply and, combined with TR-C, the agent would be Critical.
- **IT-operations agent.** Permission grants, destructive operations and changes to monitoring are [BAL-3.6](../controls/control-catalog.md#bal-3-6) classes, so they still need approval unless pre-authorized within limits at the [A3](#a3) promotion gate. Moving any class to [A4](#a4) would make the agent Critical and require [T3](#t3) and an [A4](#a4) authorization approved by an executive risk owner. [A4](#a4) is prohibited outright while the agent reaches restricted data.

A complete control-by-control assessment of one asset is in the [worked example](worked-example.md).

## What [T1](#t1) means in practice

Asset-scope controls for five common asset types, with the tags shown:

| Asset type | Tags | Asset [T1](#t1) | Added [T2](#t2) if rated High or Critical | [T3](#t3) (required only at [A4](#a4)) |
|---|---|---|---|---|
| Embedded SaaS copilot (vendor-operated) | RAG, UNTRUSTED, MEM | 15 | 3 | 0 |
| Internal RAG assistant built in-house | BUILT, RAG | 21 | 16 | 1 |
| AI coding agent on endpoints | CODE, ENDPOINT, AGENT, ACT, EXEC, EXT, UNTRUSTED | 28 | 9 | 1 |
| Custom autonomous agent | BUILT, AGENT, ACT, AUTO, UNTRUSTED, RAG, EXT, MEM | 43 | 27 | 3 |
| Self-hosted model application | BUILT, MODEL, INFRA, RAG | 27 | 19 | 1 |

The coding agent (EXEC) and the custom autonomous agent (AUTO, so [A3](#a3)) always meet TR-B, so they are always at least High and always carry their [T2](#t2) controls.

**Program and vendor baseline.** These controls are implemented once, not per asset:

- **23 unconditional [T1](#t1) controls** for every organization: [BAL-1.1](../controls/control-catalog.md#bal-1-1), [1.2](../controls/control-catalog.md#bal-1-2), [1.3](../controls/control-catalog.md#bal-1-3), [1.8](../controls/control-catalog.md#bal-1-8), [1.10](../controls/control-catalog.md#bal-1-10), [1.13](../controls/control-catalog.md#bal-1-13), [2.5](../controls/control-catalog.md#bal-2-5), [2.6](../controls/control-catalog.md#bal-2-6), [2.7](../controls/control-catalog.md#bal-2-7), [3.8](../controls/control-catalog.md#bal-3-8), [4.5](../controls/control-catalog.md#bal-4-5), [6.17](../controls/control-catalog.md#bal-6-17), [7.3](../controls/control-catalog.md#bal-7-3), [7.4](../controls/control-catalog.md#bal-7-4), [8.7](../controls/control-catalog.md#bal-8-7), [8.8](../controls/control-catalog.md#bal-8-8), [8.9](../controls/control-catalog.md#bal-8-9), [8.10](../controls/control-catalog.md#bal-8-10) and [8.12](../controls/control-catalog.md#bal-8-12) (Program), and [BAL-8.2](../controls/control-catalog.md#bal-8-2), [8.3](../controls/control-catalog.md#bal-8-3), [8.4](../controls/control-catalog.md#bal-8-4) and [8.5](../controls/control-catalog.md#bal-8-5) (Vendor, assessed once per vendor, service and plan).
- **10 conditional [T1](#t1) controls** that apply when the organization has the tagged assets: [BAL-1.9](../controls/control-catalog.md#bal-1-9) and [6.20](../controls/control-catalog.md#bal-6-20) (ENDPOINT), [BAL-1.11](../controls/control-catalog.md#bal-1-11) (LOWCODE), [BAL-5.16](../controls/control-catalog.md#bal-5-16) and [5.18](../controls/control-catalog.md#bal-5-18) (EXT), [BAL-5.17](../controls/control-catalog.md#bal-5-17) (EXT or CODE), [BAL-5.20](../controls/control-catalog.md#bal-5-20), [5.21](../controls/control-catalog.md#bal-5-21) and [5.22](../controls/control-catalog.md#bal-5-22) (CODE), and [BAL-6.16](../controls/control-catalog.md#bal-6-16) (CODE or ENDPOINT).

An organization whose only AI asset is an embedded copilot therefore implements 23 baseline controls once and 15 asset controls for the copilot. A copilot that reads email is usually rated High (TR-C), which adds its 3 asset [T2](#t2) controls and the Program and Vendor [T2](#t2) controls whose tags it carries ([BAL-1.14](../controls/control-catalog.md#bal-1-14), [7.12](../controls/control-catalog.md#bal-7-12) and [8.11](../controls/control-catalog.md#bal-8-11), and [BAL-8.6](../controls/control-catalog.md#bal-8-6) for the vendor).

## Distribution

By domain and [Control Tier](#control-tiers):

| # | Domain | Controls | [T1](#t1) | [T2](#t2) | [T3](#t3) |
|---|---|---|---|---|---|
| 1 | [AI Governance, Inventory & Classification](../framework/domains/01-ai-governance-inventory-and-classification.md) | 15 | 14 | 1 | 0 |
| 2 | [Agent Identity, Authentication & Lifecycle](../framework/domains/02-agent-identity-authentication-and-lifecycle.md) | 13 | 8 | 4 | 1 |
| 3 | [Delegated Authorization & Least Agency](../framework/domains/03-delegated-authorization-and-least-agency.md) | 13 | 8 | 5 | 0 |
| 4 | [Data Security, Provenance & Trust](../framework/domains/04-data-security-provenance-and-trust.md) | 16 | 9 | 6 | 1 |
| 5 | [Secure AI SDLC & Supply Chain](../framework/domains/05-secure-ai-sdlc-and-supply-chain.md) | 23 | 16 | 7 | 0 |
| 6 | [Runtime Guardrails & Containment](../framework/domains/06-runtime-guardrails-and-containment.md) | 22 | 13 | 8 | 1 |
| 7 | [Observability, Detection & Response](../framework/domains/07-observability-detection-and-response.md) | 13 | 4 | 8 | 1 |
| 8 | [Third-Party, Vendor & Shadow AI Risk](../framework/domains/08-third-party-vendor-and-shadow-ai-risk.md) | 13 | 11 | 2 | 0 |
| | **Total** | **128** | **83** | **41** | **4** |

By scope and [Control Tier](#control-tiers):

| Scope | Controls | [T1](#t1) | [T2](#t2) | [T3](#t3) |
|---|---|---|---|---|
| Asset | 86 | 50 | 33 | 3 |
| Program | 37 | 29 | 7 | 1 |
| Vendor | 5 | 4 | 1 | 0 |
| **Total** | **128** | **83** | **41** | **4** |

Counts are taken from the control catalog. If a count here differs from [control-catalog.csv](../controls/control-catalog.csv), the CSV is authoritative.

## Exceptions and risk acceptance

Not applicable is decided by the asset's tags. Tailoring and risk acceptance require approval under [BAL-1.13](../controls/control-catalog.md#bal-1-13). [A4](#a4) authorization is separate and does not excuse unmet controls.

| Mechanism | When it is used | Approval | Maximum duration | How it counts |
|---|---|---|---|---|
| **Not applicable** | The asset's tags do not satisfy the control's applies-to expression. | None; derived from tags | None; re-derived whenever tags change | Excluded from the asset's applicable controls. Not an exception. |
| **[T2](#t2) tailoring** | A [T2](#t2) control required for a High or Critical asset is replaced by a documented compensating control that addresses the same risk. | Approver whose authority matches the asset's risk rating | 12 months | Met by the compensating control while in date; reported as tailored, not as implemented |
| **[A4](#a4) authorization** | Permission to operate at [A4](#a4) while all required controls are met. It does not excuse a gap. | Executive risk owner, through the [BAL-3.1](../controls/control-catalog.md#bal-3-1) promotion gate | 6 months; each renewal needs a new promotion gate | Does not make a satisfied control Excepted; operation stops at expiry |
| **Risk acceptance** | An applicable [T1](#t1) control is not met, or a [T2](#t2) control is not met and no compensating control exists. | Approver whose authority scales with the asset's risk rating | 6 months for High or Critical assets; 12 months for Low or Medium. One renewal, only with a funded remediation plan. | Always counted as a gap |

Rules that apply to every tailoring and risk acceptance:

- Each is recorded in the central register ([BAL-1.13](../controls/control-catalog.md#bal-1-13); see the [exceptions log template](exceptions-log-template.csv)) with the control, the asset, the residual risk, the compensating controls, a risk-register reference, the approver and the expiry date.
- Approver authority scales with the asset's risk rating, under the decision rights set in [BAL-1.2](../controls/control-catalog.md#bal-1-2). For example: the asset owner's accountable executive for Low or Medium, the CISO or a delegate for High, and an executive risk owner for Critical. For a Program or Vendor control, use the highest rating among the assets that inherit it.
- When a tailoring or risk acceptance expires without re-approval, the control reverts to an open gap. There is no grace period.
- Renew tailoring only with fresh approval and current evidence for the compensating control.
- The register is reviewed at least quarterly.
- The controls listed below cannot be tailored or risk-accepted.

## Non-acceptable controls

For a production asset, the following controls cannot be tailored or risk-accepted where they apply. An asset that does not meet one of them is not released to production, or is suspended until it does.

| Control | Where it applies | What must be true |
|---|---|---|
| [BAL-1.4](../controls/control-catalog.md#bal-1-4) Human owner of record | Every asset | A named, current owner is accountable for the asset. |
| [BAL-1.5](../controls/control-catalog.md#bal-1-5) AI asset risk rating and capability profile | Every asset | The asset is rated and tagged, so the rest of its controls can be derived. |
| [BAL-1.6](../controls/control-catalog.md#bal-1-6) AI intake and registration gate | Every asset | The asset is registered and approved through the workflow its rating requires. The only exception route is the one [BAL-1.6](../controls/control-catalog.md#bal-1-6) itself provides: a vendor-enabled feature that could not be held off may be excepted under [BAL-1.13](../controls/control-catalog.md#bal-1-13) while it is brought into intake within the defined period. |
| [BAL-2.4](../controls/control-catalog.md#bal-2-4) Agent credential storage, lifetime and revocation | AGENT, EXT | Credentials stay out of prompts, context, memory, code, logs and configuration files, expire, and can be revoked. |
| [BAL-3.5](../controls/control-catalog.md#bal-3-5) Untrusted-input capability separation (the decision) | UNTRUSTED | The A/B/C profile is recorded, and the asset drops one property, constrains each outbound action deterministically, routes it through [BAL-3.6](../controls/control-catalog.md#bal-3-6) approval, or splits the workflow. The owner chooses the response; having none is not acceptable. |
| [BAL-3.6](../controls/control-catalog.md#bal-3-6) Human approval of high-risk actions | Where the asset has any high-risk action class | High-risk actions wait for approval rendered by the enforcement point, or are pre-authorized within limits at an [A3](#a3) promotion gate. |
| [BAL-3.7](../controls/control-catalog.md#bal-3-7) Agent kill switch | AGENT | An authorized operator can halt the agent within the defined time objective. |
| [BAL-6.1](../controls/control-catalog.md#bal-6-1) Authority set outside the model | BUILT+AGENT | Tools, scopes, recipients and data sources are set outside the model, and content cannot widen them. |
| [BAL-6.13](../controls/control-catalog.md#bal-6-13) Agent execution isolation | EXEC | Code and tool execution runs inside an isolation boundary enforced outside the agent. |
| [BAL-7.1](../controls/control-catalog.md#bal-7-1) Agent action audit log | AGENT | Every agent action is logged by the enforcement point, not by the agent. For a vendor-operated agent, the vendor audit log is enabled and exported; individual missing fields are recorded as a partial gap, but an absent or disabled log blocks production. |
| [BAL-8.2](../controls/control-catalog.md#bal-8-2) Vendor training-use commitment | Where the vendor service processes restricted data | The vendor does not train on the organization's data, and the accounts, plans and settings in use honor that commitment. |

**[A4](#a4) prohibitions.** No action class may run at [A4](#a4) for an asset that makes or materially supports consequential decisions about individuals, reaches restricted data, can take irreversible financial actions, or does not meet [BAL-3.5](../controls/control-catalog.md#bal-3-5). Where [A4](#a4) is permitted, it needs an [A4](#a4) authorization ([BAL-1.13](../controls/control-catalog.md#bal-1-13)) approved by an executive risk owner, and its conditions (all applicable [T2](#t2) and [T3](#t3) controls implemented, [BAL-3.7](../controls/control-catalog.md#bal-3-7) tested) cannot be tailored or risk-accepted. An [A4](#a4) authorization lasts at most 6 months and is renewed only through a new promotion gate record ([BAL-3.1](../controls/control-catalog.md#bal-3-1)); the one-renewal limit for risk acceptances does not apply to it. [A4](#a4) operation must stop when its authorization expires.

## Pilot minimum

Pilots and developer tools using real organizational data, identities, credentials or users must meet the following applicable controls before their first real use.

| Control | What it means for a pilot |
|---|---|
| [BAL-1.1](../controls/control-catalog.md#bal-1-1) AI security policy and acceptable use | The pilot is a permitted use, and its users have acknowledged the policy. |
| [BAL-1.4](../controls/control-catalog.md#bal-1-4) Human owner of record | The pilot has a named owner. |
| [BAL-1.5](../controls/control-catalog.md#bal-1-5) AI asset risk rating and capability profile | The pilot is tagged and rated. |
| [BAL-1.6](../controls/control-catalog.md#bal-1-6) AI intake and registration gate | The pilot is registered and approved before it touches real data. |
| [BAL-2.4](../controls/control-catalog.md#bal-2-4) Agent credential storage, lifetime and revocation | Its credentials are stored, limited and revocable. |
| [BAL-3.6](../controls/control-catalog.md#bal-3-6) Human approval of high-risk actions | High-risk actions wait for a person. |
| [BAL-3.7](../controls/control-catalog.md#bal-3-7) Agent kill switch | It can be halted. |
| [BAL-4.5](../controls/control-catalog.md#bal-4-5) DLP coverage of AI channels | Its channels are on the DLP coverage map. |
| [BAL-7.1](../controls/control-catalog.md#bal-7-1) Agent action audit log | Its actions are logged by the enforcement point. |
| [BAL-8.2](../controls/control-catalog.md#bal-8-2) Vendor training-use commitment | The vendor service does not train on the pilot's data. |
| [BAL-8.7](../controls/control-catalog.md#bal-8-7) AI vendor, plan and model risk profiling | The vendor, plan and model are profiled for the data classes the pilot uses. |
| [BAL-3.5](../controls/control-catalog.md#bal-3-5) Untrusted-input capability separation (where UNTRUSTED) | The separation decision is made before the pilot reads untrusted content. |
| [BAL-6.1](../controls/control-catalog.md#bal-6-1) Authority set outside the model (where BUILT+AGENT and UNTRUSTED) | Content the pilot reads cannot add tools, widen scopes or change recipients. |
| [BAL-6.13](../controls/control-catalog.md#bal-6-13) Agent execution isolation (where EXEC) | Code, commands and file access run inside an isolation boundary with no ambient credentials. |

The complete applicable [T1](#t1) must be implemented at the production release or 90 days following the initial real-data usage, whichever occurs sooner. From that moment onward, the pilot is considered a production asset: it is subject to the full applicable [T1](#t1), and additionally, [T2](#t2) applies if the pilot is rated as High or Critical.

## Vendor-operated assets

For vendor-operated AI, such as an embedded SaaS copilot or a vendor-hosted agent, responsibility is shared. Many enforcement points sit inside the vendor's service, where the organization cannot implement or inspect them directly.

| Who | What | How it is recorded |
|---|---|---|
| The organization configures | Tenant and platform settings, sharing, connectors, memory and rendering lists ([BAL-6.17](../controls/control-catalog.md#bal-6-17)); labels and DLP ([BAL-4.1](../controls/control-catalog.md#bal-4-1), [BAL-4.5](../controls/control-catalog.md#bal-4-5)); grounding scope ([BAL-4.8](../controls/control-catalog.md#bal-4-8)); owner, rating and intake ([BAL-1.4](../controls/control-catalog.md#bal-1-4) to [BAL-1.6](../controls/control-catalog.md#bal-1-6)) | Implemented |
| The vendor enforces inside its service | For example trust separation ([BAL-3.5](../controls/control-catalog.md#bal-3-5)), output rendering limits ([BAL-6.3](../controls/control-catalog.md#bal-6-3)), injection detection for agents built on a vendor platform ([BAL-6.4](../controls/control-catalog.md#bal-6-4)), action logging ([BAL-7.1](../controls/control-catalog.md#bal-7-1)) and the halt mechanism ([BAL-3.7](../controls/control-catalog.md#bal-3-7)) | Provider-implemented (evidenced) |
| The vendor commits by contract | Training use, isolation and retention, incident notification and assurance ([BAL-8.2](../controls/control-catalog.md#bal-8-2) to [BAL-8.5](../controls/control-catalog.md#bal-8-5)) | Vendor-scope controls, assessed once per vendor, service and plan |

Rules for vendor-operated assets:

- A control whose enforcement point sits inside the vendor's service still applies if the asset's tags say so. It is never Not applicable for that reason.
- "Provider-implemented (evidenced)" counts toward coverage only with evidence specific to the control: vendor documentation mapped to the control, an independent attestation whose scope covers the feature in use ([BAL-8.5](../controls/control-catalog.md#bal-8-5)), or the organization's own test, such as a canary injection or a rendering test. A general assurance report that does not cover the AI feature is not enough.
- Evidence comes from the organization's tenant configuration ([BAL-6.17](../controls/control-catalog.md#bal-6-17)) and from the vendor. For High or Critical assets tagged UNTRUSTED or ACT whose agent runtime, tool or connector execution, outbound requests or output rendering the vendor operates, [BAL-8.6](../controls/control-catalog.md#bal-8-6) requires a structured review of the vendor's injection and exfiltration defenses and of which actions the vendor lets the organization export to its own logs.
- Report provider-implemented controls separately from controls the organization implements itself, so leaders can see how much of the posture depends on vendors.
- Where a vendor provides no usable evidence, record a gap with a compensating control (for example restricting grounding scope, disabling external image rendering, or turning the feature off for groups that handle restricted data) or a risk acceptance under [BAL-1.13](../controls/control-catalog.md#bal-1-13), unless the control is non-acceptable.

## Relationship to other models

[CIS Controls](https://www.cisecurity.org/controls) implementation groups reflect organizational risk and resources; [NIST SP 800-53B](https://csrc.nist.gov/pubs/sp/800/53/b/upd1/final) baselines reflect information-system impact. Ballast [Control Tiers](#control-tiers) are selected per AI asset using risk and capability tags.

Back to the [framework overview](../README.md).
