# Adoption and Assessment Guide

This guide explains how to adopt Ballast v1.0.0: the order in which to put controls in place, how to run an assessment with the templates, how to measure and report progress, and how to describe the result. It relies on the capability tags, [Control Tiers](tiering.md#control-tiers), risk rating, [autonomy levels](tiering.md#autonomy-levels) and exception rules in [Control Tiers](tiering.md). Terms are defined in the [glossary](../framework/glossary.md).

## Adoption path

| Step | Action | Ballast reference |
|---|---|---|
| 1 | Define scope. | [What is in scope](tiering.md#tiers) |
| 2 | Stand up the Program [T1](tiering.md#t1) baseline, including vendor controls. | [BAL-1.1](../controls/control-catalog.md#bal-1-1) to [1.3](../controls/control-catalog.md#bal-1-3), [1.8](../controls/control-catalog.md#bal-1-8) to [1.11](../controls/control-catalog.md#bal-1-11), [1.13](../controls/control-catalog.md#bal-1-13), [2.5](../controls/control-catalog.md#bal-2-5) to [2.7](../controls/control-catalog.md#bal-2-7), [3.8](../controls/control-catalog.md#bal-3-8), [4.5](../controls/control-catalog.md#bal-4-5), [5.16](../controls/control-catalog.md#bal-5-16) to [5.18](../controls/control-catalog.md#bal-5-18), [5.20](../controls/control-catalog.md#bal-5-20) to [5.22](../controls/control-catalog.md#bal-5-22), [6.16](../controls/control-catalog.md#bal-6-16), [6.17](../controls/control-catalog.md#bal-6-17), [6.20](../controls/control-catalog.md#bal-6-20), [7.3](../controls/control-catalog.md#bal-7-3), [7.4](../controls/control-catalog.md#bal-7-4), [8.2](../controls/control-catalog.md#bal-8-2) to [8.5](../controls/control-catalog.md#bal-8-5), [8.7](../controls/control-catalog.md#bal-8-7) to [8.10](../controls/control-catalog.md#bal-8-10), [8.12](../controls/control-catalog.md#bal-8-12) |
| 3 | Register and rate every AI asset. | [BAL-1.4](../controls/control-catalog.md#bal-1-4), [1.5](../controls/control-catalog.md#bal-1-5), [1.6](../controls/control-catalog.md#bal-1-6) |
| 4 | Close each asset's [T1](tiering.md#t1) controls, as its tags require. | [Applicability](tiering.md#how-ballast-decides-which-controls-apply) |
| 5 | Add [T2](tiering.md#t2) controls for assets rated High or Critical. | [BAL-1.5](../controls/control-catalog.md#bal-1-5) |
| 6 | Add [T3](tiering.md#t3) controls for any asset with an action class at [A4](tiering.md#a4). | [BAL-3.1](../controls/control-catalog.md#bal-3-1), [BAL-1.13](../controls/control-catalog.md#bal-1-13) |
| 7 | Record every gap that will not close soon as an exception. | [BAL-1.13](../controls/control-catalog.md#bal-1-13) |
| 8 | Reassess on a cadence set by risk rating, and on every material change. | [BAL-1.5](../controls/control-catalog.md#bal-1-5), [BAL-5.2](../controls/control-catalog.md#bal-5-2), [BAL-5.5](../controls/control-catalog.md#bal-5-5) |

Domain 1 comes first because every other control attaches to an inventoried, owned and rated asset.

### 1. Define scope

In scope is every AI asset in production, and every pilot or developer tool that touches real (non-synthetic) organizational data, users, identities or credentials. That includes AI features embedded in approved SaaS, copilots and assistants, AI coding assistants and agents, low-code agents, custom AI applications and agents, externally sourced models and self-hosted AI services. Pilots start from the [pilot minimum](tiering.md#pilot-minimum). Write the scope down: the inventory completeness metric is measured against it.

### 2. Stand up the Program [T1](tiering.md#t1) baseline

Program and Vendor controls are implemented once and inherited by every asset, so they come before asset work.

| Purpose | Controls | Required when |
|---|---|---|
| Set the rules | [BAL-1.1](../controls/control-catalog.md#bal-1-1) AI security policy and acceptable use; [BAL-1.2](../controls/control-catalog.md#bal-1-2) roles and decision rights; [BAL-1.3](../controls/control-catalog.md#bal-1-3) role-based training | Always |
| Handle exceptions | [BAL-1.13](../controls/control-catalog.md#bal-1-13) exception and risk-acceptance workflow | Always |
| Find what is in use | [BAL-1.8](../controls/control-catalog.md#bal-1-8) model and AI provider usage inventory; [BAL-1.10](../controls/control-catalog.md#bal-1-10) embedded SaaS AI inventory; [BAL-1.9](../controls/control-catalog.md#bal-1-9) endpoint AI discovery | Always, except [BAL-1.9](../controls/control-catalog.md#bal-1-9) (ENDPOINT) |
| Control identity and third-party access | [BAL-2.5](../controls/control-catalog.md#bal-2-5) enterprise identity plane; [BAL-2.6](../controls/control-catalog.md#bal-2-6) third-party AI app consent; [BAL-2.7](../controls/control-catalog.md#bal-2-7) third-party AI grant inventory and revocation | Always |
| Map the data channels | [BAL-4.5](../controls/control-catalog.md#bal-4-5) DLP coverage of AI channels | Always |
| Govern vendors | [BAL-8.7](../controls/control-catalog.md#bal-8-7) vendor, plan and model profiling; [BAL-8.8](../controls/control-catalog.md#bal-8-8) vendor change monitoring; [BAL-8.12](../controls/control-catalog.md#bal-8-12) supplier AI use; [BAL-8.2](../controls/control-catalog.md#bal-8-2) to [8.5](../controls/control-catalog.md#bal-8-5), assessed once per vendor, service and plan | Always |
| Contain unsanctioned AI | [BAL-8.9](../controls/control-catalog.md#bal-8-9) prevention and detection; [BAL-8.10](../controls/control-catalog.md#bal-8-10) shadow AI response and approved catalog | Always |
| Operate and respond | [BAL-3.8](../controls/control-catalog.md#bal-3-8) spend ceilings; [BAL-6.17](../controls/control-catalog.md#bal-6-17) AI platform and SaaS tenant baseline; [BAL-7.3](../controls/control-catalog.md#bal-7-3) event forwarding and telemetry health; [BAL-7.4](../controls/control-catalog.md#bal-7-4) AI incident response playbooks | Always |
| Govern components, coding tools and builders | [BAL-5.16](../controls/control-catalog.md#bal-5-16), [5.17](../controls/control-catalog.md#bal-5-17), [5.18](../controls/control-catalog.md#bal-5-18) (EXT); [BAL-5.20](../controls/control-catalog.md#bal-5-20), [5.21](../controls/control-catalog.md#bal-5-21), [5.22](../controls/control-catalog.md#bal-5-22) (CODE); [BAL-6.16](../controls/control-catalog.md#bal-6-16) (CODE or ENDPOINT); [BAL-6.20](../controls/control-catalog.md#bal-6-20) (ENDPOINT); [BAL-1.11](../controls/control-catalog.md#bal-1-11) (LOWCODE) | When any in-scope asset carries the tag |

That is 23 unconditional controls (19 Program, 4 Vendor) and 10 conditional ones. A tag counts when any in-scope asset carries it, including unsanctioned use found by discovery: if developers use unsanctioned coding agents, the organization has CODE assets.

### 3. Register and rate every asset

Record each asset in the [asset register](asset-register-template.csv) with a named owner ([BAL-1.4](../controls/control-catalog.md#bal-1-4)), its capability tags, its [autonomy level](tiering.md#autonomy-levels) for each action class, its initiation mode, its Rule of Two profile if it is tagged UNTRUSTED ([BAL-3.5](../controls/control-catalog.md#bal-3-5)), its data classes and its risk rating under the [BAL-1.5](../controls/control-catalog.md#bal-1-5) rubric. New assets and newly enabled AI features pass the intake gate ([BAL-1.6](../controls/control-catalog.md#bal-1-6)) before they reach production users or data. Vendor features that were switched on before they could be held off are brought into intake within a defined period or excepted ([BAL-1.6](../controls/control-catalog.md#bal-1-6), [BAL-1.10](../controls/control-catalog.md#bal-1-10)). An asset that nobody will own is suspended or decommissioned ([BAL-1.4](../controls/control-catalog.md#bal-1-4), [BAL-1.15](../controls/control-catalog.md#bal-1-15)).

Tag what the asset can do as deployed, not what it is usually asked to do. A missed tag hides controls.

### 4. Close asset [T1](tiering.md#t1)

For each asset, implement every [T1](tiering.md#t1) Asset control whose applies-to expression its tags satisfy. Two orderings save effort:

- **Shared platforms first.** A control implemented once on an AI gateway, an agent platform, a managed coding-agent configuration or a SaaS tenant baseline closes that control for every asset onboarded to it.
- **Riskiest assets first.** For High and Critical assets, start with the containment controls that apply: [BAL-3.5](../controls/control-catalog.md#bal-3-5), [3.6](../controls/control-catalog.md#bal-3-6), [3.7](../controls/control-catalog.md#bal-3-7), [6.1](../controls/control-catalog.md#bal-6-1), [6.3](../controls/control-catalog.md#bal-6-3), [6.13](../controls/control-catalog.md#bal-6-13), [6.14](../controls/control-catalog.md#bal-6-14), [7.1](../controls/control-catalog.md#bal-7-1) and [2.4](../controls/control-catalog.md#bal-2-4). Several of them are [non-acceptable](tiering.md#non-acceptable-controls) for production assets.

### 5. Add [T2](tiering.md#t2) for High and Critical assets

Each asset rated High or Critical also needs the [T2](tiering.md#t2) Asset controls its tags match. Program [T2](tiering.md#t2) controls become required once the inventory holds any High or Critical asset carrying the control's tags (for example [BAL-1.14](../controls/control-catalog.md#bal-1-14) risk reporting, [BAL-3.12](../controls/control-catalog.md#bal-3-12) approval effectiveness monitoring for ACT assets, [BAL-7.12](../controls/control-catalog.md#bal-7-12) attack-chain detection content), and [BAL-8.6](../controls/control-catalog.md#bal-8-6) is assessed for each vendor service that operates the agent runtime, tool execution, outbound requests or rendering of a High or Critical asset tagged UNTRUSTED or ACT. TR-C covers any asset that combines untrusted input, sensitive access and an outbound channel, including rendering, so most copilots that read email and most agents are High. Plan for [T2](tiering.md#t2) early.

### 6. Add [T3](tiering.md#t3) where any action class is at [A4](tiering.md#a4)

[T3](tiering.md#t3) is required for any asset with an action class at [A4](tiering.md#a4), recommended for Critical assets and optional otherwise. [A4](tiering.md#a4) needs a separate authorization recorded under [BAL-1.13](../controls/control-catalog.md#bal-1-13): it needs an executive risk owner's approval, all applicable [T2](tiering.md#t2) and [T3](tiering.md#t3) controls implemented and [BAL-3.7](../controls/control-catalog.md#bal-3-7) tested ([BAL-3.1](../controls/control-catalog.md#bal-3-1)). It is prohibited in the cases listed under [A4 prohibitions](tiering.md#non-acceptable-controls).

### 7. Record exceptions

Use the [exceptions log](exceptions-log-template.csv) under [BAL-1.13](../controls/control-catalog.md#bal-1-13) for three types of decision:

- **[T2](tiering.md#t2) tailoring:** a [T2](tiering.md#t2) control is replaced by a documented compensating control that addresses the same risk. Maximum 12 months. Renew only with fresh approval and current evidence for the compensating control.
- **Risk acceptance:** an applicable control is not met and the residual risk is accepted. It always counts as a gap. Maximum 6 months for High or Critical assets and 12 months otherwise, with one renewal only, backed by a funded remediation plan.

- **[A4](tiering.md#a4) authorization:** permission to operate at [A4](tiering.md#a4) while all required controls are met, approved by an executive risk owner for at most 6 months. Each renewal requires a new promotion gate. Link the approved action classes and gate record in the [BAL-3.1](../controls/control-catalog.md#bal-3-1) assessment's evidence and notes, and record the authorization reference in exception_id. [A4](tiering.md#a4) authorization does not make a satisfied control Excepted.

The approver's authority matches the asset's risk rating. [Non-acceptable controls](tiering.md#non-acceptable-controls) cannot be tailored or risk-accepted. Expired tailoring and risk acceptances revert to open gaps. [A4](tiering.md#a4) operation must stop when its authorization expires.

### 8. Reassess

**On a cadence.** The risk rating sets the review cadence ([BAL-1.5](../controls/control-catalog.md#bal-1-5)). Suggested defaults, which the organization may tighten:

| Risk rating | Full reassessment of the asset's rows |
|---|---|
| Low or Medium | At least every 12 months |
| High | At least every 6 months |
| Critical | At least every 3 months |

**On material change.** A material change re-opens registration and approval ([BAL-1.6](../controls/control-catalog.md#bal-1-6)) and the risk rating ([BAL-1.5](../controls/control-catalog.md#bal-1-5)), goes through AI change management with re-testing ([BAL-5.2](../controls/control-catalog.md#bal-5-2), [BAL-5.5](../controls/control-catalog.md#bal-5-5)), and triggers reassessment of the asset. Material changes include a new or changed model or provider, a new tool, MCP server, connector or skill, a new data source or data class, a new untrusted input path or output surface, a new user population or external users, an [autonomy promotion](tiering.md#autonomy-levels) ([BAL-3.1](../controls/control-catalog.md#bal-3-1)), and a new vendor plan or default-on feature. Evidence dated before the change counts as Not implemented until it is refreshed (see [evidence rules](#evidence-rules)). For rows the change did not touch, refreshing can mean confirming that the existing evidence still describes the asset and recording a new evidence_date; rows the change touched need new evidence.

### Assess program maturity separately

Use [CSA AISMM](https://cloudsecurityalliance.org/artifacts/ai-security-maturity-model) to assess current maturity, choose improvement priorities, assign owners and review progress regularly. Use Ballast assessments as evidence; do not treat [Control Tiers](tiering.md#control-tiers) or coverage percentages as maturity levels.

Use the optional [AISMM-based Excel scorecard](maturity/README.md) to discuss the program's current state and prioritize improvements. Save a separate copy for each assessment and rate achieved practices supported by evidence. The scorecard is a category-level aid, not a full AISMM assessment or an official CSA workbook.

## First 90 days (non-normative)

This is a suggested order of work for a program starting with little in place. It is not a [Control Tier](tiering.md#control-tiers), it does not change what any [Control Tier](tiering.md#control-tiers) requires, and finishing it does not make an organization conformant.

| Window | Focus | Work |
|---|---|---|
| Days 1 to 30 | Know what is running and close the open doors | Name the accountable executive, approvers and AI incident lead ([BAL-1.2](../controls/control-catalog.md#bal-1-2)). Publish the AI security policy and acceptable use with an initial approved catalog ([BAL-1.1](../controls/control-catalog.md#bal-1-1), [BAL-8.10](../controls/control-catalog.md#bal-8-10)). Turn on discovery of provider usage, endpoint AI, embedded SaaS AI and third-party AI grants ([BAL-1.8](../controls/control-catalog.md#bal-1-8), [1.9](../controls/control-catalog.md#bal-1-9), [1.10](../controls/control-catalog.md#bal-1-10), [2.7](../controls/control-catalog.md#bal-2-7)). Disable user self-consent to unapproved AI apps ([BAL-2.6](../controls/control-catalog.md#bal-2-6)). Set spend ceilings on every provider account and key ([BAL-3.8](../controls/control-catalog.md#bal-3-8)). Open the exception register ([BAL-1.13](../controls/control-catalog.md#bal-1-13)) and the intake gate for new AI ([BAL-1.6](../controls/control-catalog.md#bal-1-6)). |
| Days 31 to 60 | Register, rate and set the platform baselines | Register every discovered asset with an owner, tags, [autonomy](tiering.md#autonomy-levels) per action class and a risk rating, and record the Rule of Two profile for every UNTRUSTED asset ([BAL-1.4](../controls/control-catalog.md#bal-1-4), [1.5](../controls/control-catalog.md#bal-1-5), [3.5](../controls/control-catalog.md#bal-3-5)). Profile vendors, plans and models and check training use, retention and notification terms ([BAL-8.7](../controls/control-catalog.md#bal-8-7), [8.2](../controls/control-catalog.md#bal-8-2) to [8.5](../controls/control-catalog.md#bal-8-5)). Build the DLP coverage map and the AI tenant configuration baseline, and forward AI security events ([BAL-4.5](../controls/control-catalog.md#bal-4-5), [6.17](../controls/control-catalog.md#bal-6-17), [7.3](../controls/control-catalog.md#bal-7-3)). Where the organization has coding or endpoint assets, apply managed configuration lockdown, the component catalog and governed dependency intake ([BAL-6.16](../controls/control-catalog.md#bal-6-16), [5.18](../controls/control-catalog.md#bal-5-18), [5.20](../controls/control-catalog.md#bal-5-20)). Start role-based training for approvers, makers and developers ([BAL-1.3](../controls/control-catalog.md#bal-1-3)). |
| Days 61 to 90 | Contain the riskiest assets and measure | Close the containment controls that apply to High and Critical assets ([BAL-3.5](../controls/control-catalog.md#bal-3-5), [3.6](../controls/control-catalog.md#bal-3-6), [3.7](../controls/control-catalog.md#bal-3-7), [6.1](../controls/control-catalog.md#bal-6-1), [6.3](../controls/control-catalog.md#bal-6-3), [6.13](../controls/control-catalog.md#bal-6-13), [6.14](../controls/control-catalog.md#bal-6-14), [7.1](../controls/control-catalog.md#bal-7-1), [2.4](../controls/control-catalog.md#bal-2-4)). Write the AI incident playbooks and run a first tabletop exercise ([BAL-7.4](../controls/control-catalog.md#bal-7-4)). Run the first full assessment, publish baseline metrics with inventory completeness first, and record an exception with an expiry date for every gap that will not close soon. |

## Running an assessment

### The templates

| File | One row per | Purpose |
|---|---|---|
| [asset-register-template.csv](asset-register-template.csv) | AI asset | Tags, [autonomy](tiering.md#autonomy-levels), data and rating. Drives which controls apply and which [Control Tiers](tiering.md#control-tiers) are required. |
| [assessment-template.csv](assessment-template.csv) | Control per asset, plus one row per Program control and one per Vendor control per vendor service | Status, evidence and ownership of each applicable control. |
| [exceptions-log-template.csv](exceptions-log-template.csv) | Exception | The [BAL-1.13](../controls/control-catalog.md#bal-1-13) register of [T2](tiering.md#t2) tailoring, risk acceptance and [A4](tiering.md#a4) authorization. |

The asset register and exceptions log templates ship with example rows whose identifiers start with EXAMPLE. Delete them before use. The [worked example](worked-example.md) shows the three templates used together for one agent.

**Asset register columns**

| Column | How to complete it |
|---|---|
| asset_id, asset_name | A stable identifier and a recognizable name. |
| asset_type | For example: embedded SaaS AI feature, copilot or assistant, AI coding assistant or agent, low-code agent, custom AI application, custom agent, self-hosted model or AI service, AI platform. |
| hosting_model | Organization-operated, vendor-operated, or built on a vendor platform ([BAL-1.5](../controls/control-catalog.md#bal-1-5)). Selects the evidence route for vendor-operated enforcement points and shows whether [BAL-8.6](../controls/control-catalog.md#bal-8-6)'s condition arises. |
| vendor_or_platform | The vendor, service and plan, or the internal platform the asset runs on. This links the asset to Vendor rows and to platform inheritance. |
| owner | The named accountable owner ([BAL-1.4](../controls/control-catalog.md#bal-1-4)). |
| business_purpose | What the asset is for, in one sentence. |
| business_critical | Y or N, with the basis (for example a recovery objective). Decides whether [BAL-8.13](../controls/control-catalog.md#bal-8-13) applies under the conditional-requirements rule. |
| deployment_stage | Pilot (real data), Production or Retiring. |
| tags | Capability tags from [tiering.md](tiering.md#applies-to-tags), comma-separated. |
| autonomy_by_action_class | Each action class with its level ([A0](tiering.md#a0) to [A4](tiering.md#a4)), or "not permitted". |
| initiation_mode | Human-initiated, or event-triggered with the trigger source. A run triggered by external content makes the asset UNTRUSTED. |
| rule_of_two_profile | Whether the asset holds each [BAL-3.5](../controls/control-catalog.md#bal-3-5) property (A untrusted content, B sensitive access, C state change or outbound channel), and, where it holds all three, how each C action is constrained. |
| data_classes | Data classes reachable, in the organization's classification scheme. |
| restricted_data, external_users, consequential_decisions | Y or N, with a short basis. These feed TR-A, TR-C (PUBLIC) and TR-D. |
| risk_rating | Low, Medium, High or Critical, with the rules met, for example "High (TR-A, TR-C)". |
| applicable_tiers | [T1](tiering.md#t1), [T1](tiering.md#t1)+[T2](tiering.md#t2), or [T1](tiering.md#t1)+[T2](tiering.md#t2)+[T3](tiering.md#t3). |
| regulatory_notes | The [BAL-1.12](../controls/control-catalog.md#bal-1-12) classification in brief. |
| last_reviewed | Date of the last rating review (YYYY-MM-DD). |

**Exceptions log columns**

| Column | How to complete it |
|---|---|
| exception_id, control_id, asset_id | The exception, the control and the asset (or PROGRAM, or the vendor service identifier). |
| type | [T2](tiering.md#t2) tailoring, Risk acceptance or [A4](tiering.md#a4) authorization. |
| residual_risk | The risk that remains, and its level. |
| compensating_controls | The controls that address the same risk, with their own evidence. Required for [T2](tiering.md#t2) tailoring. |
| risk_register_ref | The entry in the organization's risk register. |
| risk_owner, approver, approver_authority | Who owns the risk, who approved, and the rating level whose authority the approver holds under [BAL-1.2](../controls/control-catalog.md#bal-1-2). |
| approved_date, expiry_date | Expiry no later than 12 months for tailoring; 6 months (High or Critical) or 12 months (Low or Medium) for risk acceptance; 6 months for [A4](tiering.md#a4) authorization. |
| renewal_count | Risk acceptance: 0 or 1, with a funded remediation plan for renewal. Tailoring: renew only with fresh approval and current compensating-control evidence. [A4](tiering.md#a4) authorization: renew only through a new promotion gate. Record the number of renewals. |
| remediation_plan | Required for risk acceptance, and funded for any renewal of risk acceptance. |
| status | Requested, Active, Expired or Closed. |

### Procedure

1. **Confirm the inventory.** Reconcile the asset register with the discovery sources ([BAL-1.8](../controls/control-catalog.md#bal-1-8), [1.9](../controls/control-catalog.md#bal-1-9), [1.10](../controls/control-catalog.md#bal-1-10), [2.7](../controls/control-catalog.md#bal-2-7), [8.9](../controls/control-catalog.md#bal-8-9)). Send unregistered assets to intake ([BAL-1.6](../controls/control-catalog.md#bal-1-6)) and count them in inventory completeness.
2. **Confirm tags and ratings.** Check each asset's tags against what it can actually do (tools and connectors attached, data sources, output surfaces, triggers), not against its design document. Re-rate under [BAL-1.5](../controls/control-catalog.md#bal-1-5) where tags change.
3. **Generate rows.** For each asset, create a row for every Asset control at the [Control Tiers](tiering.md#control-tiers) its rating requires: [T1](tiering.md#t1) always, [T2](tiering.md#t2) for High and Critical, [T3](tiering.md#t3) where any action class is at [A4](tiering.md#a4). Critical assets may add [T3](tiering.md#t3) rows as recommended practice; report them separately. Set applicable from the tags. Adding rows for non-matching controls, marked Not applicable, is optional but lets reviewers see the derivation. Create Program rows once, with asset_id PROGRAM, and Vendor rows once per vendor, service and plan, with the vendor service identifier as asset_id. Assets do not repeat Program and Vendor rows.
4. **Assess Program and Vendor rows once.** They feed program readiness, and every asset depends on them.
5. **Assess shared controls once.** Each asset names the program, platform or vendor providing the control in inherited_from and links to the assessment and evidence showing that the asset is covered. A gap or stale evidence in the shared control is also a gap for dependent assets. Any tailoring or risk acceptance must explicitly cover those assets and their risk ratings. A dependent asset with valid tailoring is Excepted, not Inherited; risk acceptance remains a gap.
6. **Sample large endpoint populations.** For assets deployed to many managed endpoints (coding agents, IDE and browser extensions, desktop assistants), assess the managed configuration once as a pattern, and show coverage of the whole population from management telemetry, for example the share of devices reporting the managed settings and an approved version. Where evidence has to be gathered device by device, test a random sample stratified by operating system and business unit; a suggested default is 25 devices, or every device if there are fewer. One failure: fix that device and test a second sample of the same size. Two or more failures in the first sample, or any failure in the second, mean the control is Partially implemented for the population. Record the sample size, the selection method and the results in notes.
7. **Collect evidence and set status.** Use the status values and evidence rules below. Fill target_date for Partially implemented, Not implemented and Planned. Fill exception_id for Excepted and Risk-accepted.
8. **Handle conditional requirements.** Where a control's text is conditional and the condition does not arise for an applicable asset (for example [BAL-3.13](../controls/control-catalog.md#bal-3-13) for an agent with no financial, permission-grant or irreversible production action class), record Implemented, with evidence that the condition is absent, such as the [BAL-3.3](../controls/control-catalog.md#bal-3-3) capability classification. Do not record Not applicable.
9. **Review.** Have someone other than the person who implemented a control check its status and evidence before the results are reported.

### Assessment template columns

| Column | How to complete it |
|---|---|
| control_id | The BAL ID from the [control catalog](../controls/control-catalog.csv). |
| asset_id | From the asset register; PROGRAM for Program rows; the vendor service identifier for Vendor rows. |
| applicable | Y or N, derived from tags. N only where the asset's tags do not satisfy the control's applies-to expression (for Program and Vendor rows: where no in-scope asset carries the tag). |
| status | One of the status values below, entered exactly. |
| inherited_from | For Inherited rows: PROGRAM, the platform's asset_id, or the vendor service identifier. Link the shared assessment and evidence of asset coverage in evidence. |
| evidence | Pointers an assessor can follow: configuration exports, test reports, log queries, tickets, contract clauses. Do not paste sensitive content, such as prompts containing personal data or secrets, into the file. |
| evidence_date | The date the evidence was produced or observed (YYYY-MM-DD). |
| owner | The person or role accountable for the control on this asset. |
| target_date | Required for Partially implemented, Not implemented and Planned. |
| exception_id | Required for Excepted and Risk-accepted; also record the [A4](tiering.md#a4) authorization reference on the [BAL-3.1](../controls/control-catalog.md#bal-3-1) row when applicable. Must match the exceptions log. |
| notes | Compensating controls, sampling details, conditions found absent and context; include the approved action classes for [A4](tiering.md#a4) authorization. |

### Status values

| Status | Use when | Counts as covered |
|---|---|---|
| Implemented | Every sub-requirement of the control is met for this asset, with current evidence. | Yes |
| Provider-implemented (evidenced) | The vendor operates the control for this asset, and the organization holds evidence specific to the control: vendor documentation mapped to it, an independent attestation whose scope covers the feature in use, or the organization's own test. A general assurance report that does not cover the AI feature is not enough. See [vendor-operated assets](tiering.md#vendor-operated-assets). | Yes; reported separately |
| Inherited (program) | An Asset control is delivered by a program-wide process (for example identity governance for agent identities), and the evidence shows this asset is covered by it. | Yes, while the linked shared assessment is current and shows this asset is covered |
| Inherited (platform) | An Asset control is implemented once by a shared platform the asset is onboarded to (step 5). | Yes, while the linked shared assessment is current and shows this asset is covered |
| Inherited (vendor) | An Asset control is met by a vendor service whose implementation was assessed once for every asset using that service, plan and configuration, and the evidence shows this asset uses it. | Yes, while the linked shared assessment is current and shows this asset is covered; reported separately |
| Partially implemented | Some but not all sub-requirements are met. | No |
| Not implemented | The control is not in place, or its evidence is stale. | No |
| Planned | Not implemented, with an approved plan and a target date. | No |
| Not applicable | The asset's tags do not satisfy the control's applies-to expression. Never chosen for any other reason. | Excluded from every denominator |
| Excepted | [T2](tiering.md#t2) tailoring approved under [BAL-1.13](../controls/control-catalog.md#bal-1-13) and in date (exception_id required). Only [T2](tiering.md#t2) controls can be Excepted. | No; reported as tailored |
| Risk-accepted | The control is not met and the residual risk is accepted under [BAL-1.13](../controls/control-catalog.md#bal-1-13) by an approver with authority matching the asset's rating (exception_id required). | No; counts as a gap |

A [T1](tiering.md#t1) control that is not met is a gap, or Risk-accepted. It cannot be Excepted. When tailoring or risk acceptance expires, the row returns to its underlying status, normally Not implemented or Partially implemented. [A4](tiering.md#a4) authorization does not excuse a gap; [A4](tiering.md#a4) operation stops when the authorization expires.

### Evidence rules

1. **Specific.** Evidence shows the control operating for this asset, or for the inherited source plus proof that the asset is covered by it. A policy saying something should happen is evidence for the policy control, not for the technical control.
2. **Current.** Evidence older than 12 months, or older than the asset's last material change, counts as Not implemented until it is refreshed. The evidence_date column drives this check; the date of the last material change comes from the asset's change history ([BAL-5.2](../controls/control-catalog.md#bal-5-2)) or re-registration ([BAL-1.6](../controls/control-catalog.md#bal-1-6)). For Program and Vendor rows, a material change is a change to the program process, the vendor's service or plan, or the contract.
3. **Tested where the control says tested.** For controls that require a test or exercise (for example the kill switch in [BAL-3.7](../controls/control-catalog.md#bal-3-7), revocation in [BAL-2.4](../controls/control-catalog.md#bal-2-4) and [BAL-2.7](../controls/control-catalog.md#bal-2-7), and the incident playbooks in [BAL-7.4](../controls/control-catalog.md#bal-7-4)), the evidence is the test record within the required period.
4. **Not self-reported by the agent.** An agent's own account of what it did is not evidence. Use enforcement-point logs ([BAL-7.1](../controls/control-catalog.md#bal-7-1)), the state of the system of record, or test results.
5. **Retrievable.** Another assessor can follow each pointer and reach the same conclusion.

## Measuring progress

### Counting rules

- **Covered** means Implemented, Provider-implemented (evidenced), or Inherited only while the linked shared assessment is current and shows the control is met for this asset.
- Count each asset's required control once. Do not add shared-evidence records to asset counts or coverage totals. Program and Vendor controls count once in their own scopes.
- Excepted, Partially implemented, Planned and Not implemented never count as covered. Risk-accepted counts as a gap.
- Not applicable comes only from tags and is excluded from every denominator. If a control seems not to fit an asset whose tags match it, check the tags; if they are right, the control applies.
- Stale evidence (rule 2 above) counts as Not implemented.
- Report Provider-implemented and Inherited (vendor) coverage separately from coverage the organization operates, so leaders can see how much of the posture depends on vendors.
- Report pass and fail counts next to percentages. A high implementation rate can hide a Critical asset that fails [T1](tiering.md#t1).

### Metrics

Report these in this order. Inventory completeness comes first because every other number is computed over the inventory, and a partial inventory overstates them.

| Metric | Definition |
|---|---|
| Inventory completeness | Registered in-scope assets divided by registered plus discovered-but-unregistered in-scope assets, from the discovery sources ([BAL-1.8](../controls/control-catalog.md#bal-1-8), [1.9](../controls/control-catalog.md#bal-1-9), [1.10](../controls/control-catalog.md#bal-1-10), [2.7](../controls/control-catalog.md#bal-2-7), [8.9](../controls/control-catalog.md#bal-8-9)). Also report the share of registered assets with an owner, tags and a risk rating. |
| Asset [T1](tiering.md#t1) conformance | Pass or fail for each asset: pass when every applicable [T1](tiering.md#t1) Asset control is covered. Report the number and percentage of assets passing, by risk rating (Low, Medium, High, Critical). |
| Control implementation rate | Covered rows divided by applicable required rows, by control, domain, [Control Tier](tiering.md#control-tiers) and scope. Shows which controls are hard to implement across the estate. |
| Risk-weighted coverage | Sum over assets of weight times covered required rows, divided by the sum over assets of weight times applicable required rows, with weights by asset rating: Low 1, Medium 2, High 4, Critical 8. Required rows are those at the [Control Tiers](tiering.md#control-tiers) the asset's rating requires. |
| [T2](tiering.md#t2) conformance (High and Critical assets) | For each High or Critical asset: pass when every applicable [T2](tiering.md#t2) control is covered; pass with tailoring when the only uncovered [T2](tiering.md#t2) rows are Excepted under exceptions that are in date; fail otherwise. Report the number of Excepted rows alongside. |
| Exception health | Open exceptions by type and asset rating; exceptions expired but not resolved (target zero); renewals; the share of applicable [T1](tiering.md#t1) rows that are Risk-accepted; exceptions missing a risk-register reference or an approver with the required authority. |
| Program readiness | Pass or fail for the Program [T1](tiering.md#t1) baseline (every applicable Program and Vendor [T1](tiering.md#t1) row covered), with covered rows divided by applicable rows. Track applicable Program and Vendor [T2](tiering.md#t2) rows once any High or Critical asset exists. |

### Board reporting

[BAL-1.14](../controls/control-catalog.md#bal-1-14) specifies the principal risk indicators disclosed to the responsible authority at a predetermined frequency (default quarterly): inventory completeness, [T1](tiering.md#t1) adherence by risk rating, agents categorized by the highest [autonomy level](tiering.md#autonomy-levels), overdue and expiring exceptions, the unapproved AI trend and AI incidents. Predominantly, these originate directly from the metrics mentioned earlier; the agents classified by [autonomy level](tiering.md#autonomy-levels) are sourced from the asset register (highest level spanning action classes); the unapproved AI trend is derived from [BAL-8.9](../controls/control-catalog.md#bal-8-9); and AI incidents are obtained from [BAL-7.4](../controls/control-catalog.md#bal-7-4). [BAL-1.14](../controls/control-catalog.md#bal-1-14) functions as a Program [T2](tiering.md#t2) control, thereby becoming mandatory as soon as the inventory includes a High or Critical asset.

## Claiming conformance

Ballast has no certification scheme, no accredited assessors and no "Ballast-certified" status. An organization may self-assess and state the result in this form:

> Self-assessed against Ballast v1.0.0, [T1](tiering.md#t1) scope, `YYYY-MM-DD`

followed by the assets in scope (the whole inventory, or a named division or set of assets) and the inventory completeness figure for that scope.

- **[T1](tiering.md#t1) scope** means: the Program [T1](tiering.md#t1) baseline passes (program readiness), every asset in the stated scope passes asset [T1](tiering.md#t1) conformance, and no evidence relied on is stale. A Risk-accepted [T1](tiering.md#t1) row means that asset fails; there is no "[T1](tiering.md#t1) with exceptions".
- **[T1](tiering.md#t1) + [T2](tiering.md#t2) scope** adds: every High and Critical asset in scope passes [T2](tiering.md#t2) conformance, and every applicable Program and Vendor [T2](tiering.md#t2) control is covered or has valid approved [T2](tiering.md#t2) tailoring. Label any such claim "with [T2](tiering.md#t2) tailoring" and identify the affected controls and assets. Tailoring never counts as implemented coverage and cannot satisfy required [A4](tiering.md#a4) controls.
- **[T3](tiering.md#t3).** Name the assets and the [T3](tiering.md#t3) controls they meet.
- **Name the exact version.** A claim against v1.0.0 stays a claim against v1.0.0; it does not carry over to later versions.
- **Independent review** by an internal audit function or a third party can be described factually (who reviewed, what scope, when). It is still not a certification.
- A claim is not a statement of compliance with any law, regulation or other standard.
- Adapted versions of Ballast must be marked as modified (CC BY 4.0) and should not be presented as Ballast itself.

Back to the [framework overview](../README.md).
