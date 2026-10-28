# Worked Example: One Agent, End to End (illustrative)

> **Hypothetical.** The organization, systems, volumes, roles, identifiers and evidence below are invented to show how Ballast v1.0.0 is applied to one asset. No real company, product or incident is described.

This example follows one agent through the [adoption path](adoption.md): tagging, the Rule of Two decision, risk rating, deriving the applicable controls, the controls that break the main attack path, and a few completed assessment rows. The same agent appears as EXAMPLE-AST-002 in the [asset register template](asset-register-template.csv), and its tailoring decision as EXAMPLE-EXC-001 in the [exceptions log template](exceptions-log-template.csv).

## The asset

A mid-sized insurer builds a claims-intake agent for its claims operations team.

1. Each new email to the dedicated claims mailbox triggers a run. The trigger is a mail-flow subscription owned by the agent's deployment.
2. The agent reads the message subject and body, text extracted from attachments (claim forms, medical notes) and text extracted from images (photos of documents).
3. It calls `policy_lookup` to confirm that the policy is in force. The tool takes one policy number and returns the policy status, cover type and insured name.
4. It prepares a draft claim record and proposes it through `create_draft_claim`. The claims system shows the proposed record to an adjuster, who approves or rejects it. Only approved records are written. Each write carries both the agent's identity and the approving adjuster's identity.
5. Each email is handled in a fresh session, with no memory of earlier emails.

The two tools are served by two internal MCP servers (policy administration and claims) that the integration platform team operates. The model is provider-hosted and reached through the organization's AI gateway. The agent does not reply to claimants, browse the web, run code, write files or call other agents.

The agent is in production. It handles about 1,500 emails a week, and about 40 adjusters approve its drafts.

## Step 1: Tags

| Tag | Carried | Why |
|---|---|---|
| BUILT | Yes | The organization builds and configures the agent, its prompts and its tools. |
| AGENT | Yes | It calls tools. |
| ACT | Yes | `create_draft_claim` changes state, at [A2](tiering.md#a2). |
| UNTRUSTED | Yes | Anyone can email the claims mailbox, and runs are triggered by that external content. Tool output from `policy_lookup` is also content the organization did not fully author. |
| EXT | Yes | It uses MCP servers. |
| RAG | No | It does not search or ground on indexed enterprise content. Its only enterprise read is a single-record tool lookup, governed as a tool ([BAL-3.2](../controls/control-catalog.md#bal-3-2), [3.3](../controls/control-catalog.md#bal-3-3), [3.4](../controls/control-catalog.md#bal-3-4)). Adding a knowledge base of claims-handling guidance would add RAG, and with it [BAL-4.7](../controls/control-catalog.md#bal-4-7), [4.8](../controls/control-catalog.md#bal-4-8) and [4.9](../controls/control-catalog.md#bal-4-9) at [T1](tiering.md#t1). |
| MEM | No | Nothing persists between sessions. |
| AUTO | No | No action class runs at [A3](tiering.md#a3) or above. |
| EXEC | No | It does not run code or shell commands, or perform model-directed filesystem writes. |
| MULTI | No | It neither calls nor is called by other agents. |
| MODEL | No | The model is provider-hosted; the organization holds no weights. |
| INFRA | No | The MCP servers and the AI gateway are self-hosted AI services, but they are registered as their own platform assets and shared with other agents, so [BAL-6.19](../controls/control-catalog.md#bal-6-19) is assessed there. The agent's own [BAL-2.8](../controls/control-catalog.md#bal-2-8) row covers it as an MCP client. |
| CODE, ENDPOINT, LOWCODE | No | It is not a coding tool, does not run on endpoints and was not built in a low-code builder. |
| PUBLIC | No | Claimants send email but do not use the agent. Their content is covered by UNTRUSTED. |

**Tags: BUILT, AGENT, ACT, UNTRUSTED, EXT.**

[Autonomy](tiering.md#autonomy-levels) is recorded per action class under [BAL-1.5](../controls/control-catalog.md#bal-1-5) and enforced under [BAL-3.1](../controls/control-catalog.md#bal-3-1):

| Action class | Level | How it is enforced |
|---|---|---|
| Read new messages in the claims mailbox | [A0](tiering.md#a0) | Read-only connector scoped to one mailbox |
| `policy_lookup` | [A0](tiering.md#a0) | Read-only scope on the policy MCP server |
| `create_draft_claim` | [A2](tiering.md#a2) | Each write waits for an adjuster's approval on a screen rendered by the claims system |
| Replies to claimants, payments, any other write | Not permitted | No such tool exists, and the tool allowlist denies anything else |

Initiation mode: event-triggered by inbound email, which counts as UNTRUSTED.

## Step 2: Rule of Two profile ([BAL-3.5](../controls/control-catalog.md#bal-3-5))

| Property | Held | What |
|---|---|---|
| A: attacker-influenceable content | Yes | Email subjects, bodies and attachments from any sender; `policy_lookup` output, some of whose fields were entered by customers |
| B: sensitive data or systems | Yes | Claimant personal data, including health and injury details (Restricted); policy records; write access to the claims system |
| C: state change or outbound channel | Yes | `create_draft_claim` writes; the adjuster review screen renders model output, so links and images are an outbound channel |

The workflow needs all three, so [BAL-3.5](../controls/control-catalog.md#bal-3-5) requires each C action to be constrained by a deterministic control the model cannot alter, approved under [BAL-3.6](../controls/control-catalog.md#bal-3-6), or removed by splitting the workflow. The owner chose approval and deterministic constraints:

| C channel | How it is constrained | Control |
|---|---|---|
| Draft-claim writes | Every write is approved by an adjuster under [BAL-3.6](../controls/control-catalog.md#bal-3-6). The claims system, not the model, shows the exact field values, with hidden and confusable characters revealed. Approval is single-use and bound to a hash of the parameters. The tool's argument schema fixes the fields and their formats, and the policy number in the draft must match the policy returned by `policy_lookup`. | [BAL-3.6](../controls/control-catalog.md#bal-3-6), [BAL-3.2](../controls/control-catalog.md#bal-3-2) |
| Rendering in the review screen | Model output is rendered as plain text. Remote images, link previews and other automatically fetched resources are not loaded; links are inert and show their full destination. | [BAL-6.3](../controls/control-catalog.md#bal-6-3) |
| Any other network path | Runtime egress is default-deny, with an allowlist of four hosts (the AI gateway, the two MCP servers and the mail API) enforced at the network layer, and DNS resolution only through the filtering resolver. | [BAL-6.14](../controls/control-catalog.md#bal-6-14) |
| Model inference | The endpoint is fixed in configuration and reached through the AI gateway, inside the processing boundary approved for this data by the vendor controls ([BAL-8.2](../controls/control-catalog.md#bal-8-2) to [8.5](../controls/control-catalog.md#bal-8-5)) and the [BAL-8.7](../controls/control-catalog.md#bal-8-7) profile. The model cannot redirect it. | [BAL-6.14](../controls/control-catalog.md#bal-6-14), [BAL-8.7](../controls/control-catalog.md#bal-8-7) |

There is no memory write, URL fetch or outbound email tool. `policy_lookup` is not a C channel: it is read-only, its server is internal, and its schema accepts only a policy number in the organization's format, so it cannot carry free text out.

The profile is recorded with the [BAL-1.5](../controls/control-catalog.md#bal-1-5) rating and is verified before release by [BAL-5.4](../controls/control-catalog.md#bal-5-4) testing, including canary exfiltration attempts on each untrusted input path.

## Step 3: Risk rating ([BAL-1.5](../controls/control-catalog.md#bal-1-5))

| Input | Finding |
|---|---|
| Reach | Claims operations: about 40 adjusters, and every first-notice-of-loss email |
| Exposure | Untrusted input from any sender; no external users |
| Access | Restricted claimant data, including health and injury details; policy records; claims-system writes (approved) |
| Agency | [A0](tiering.md#a0) for reads; [A2](tiering.md#a2) for draft-claim writes |
| Consequential use | Intake only. The agent does not recommend coverage, set reserves, score fraud or route claims for decision; adjusters decide from the source documents. Recorded under [BAL-1.12](../controls/control-catalog.md#bal-1-12) and confirmed by the AI governance owner. |

| Rule | Met | Basis |
|---|---|---|
| TR-A Restricted data | Yes | Health and injury data is Restricted in the organization's classification scheme. |
| TR-B [Autonomy](tiering.md#autonomy-levels) or execution | No | No action class at [A3](tiering.md#a3) or above, and no EXEC. |
| TR-C Untrusted-input combination | Yes | It holds A, B and C in one session. The constraints in step 2 make it acceptable to run; they do not remove TR-C. |
| TR-D Consequential use | No | Intake only. |

**Rating: High (TR-A, TR-C). Required [Control Tiers](tiering.md#control-tiers): [T1](tiering.md#t1) + [T2](tiering.md#t2).** The agent is not Critical: no action class is at [A4](tiering.md#a4), and TR-D is not met. [T3](tiering.md#t3) is optional.

What would change the rating:

- If the agent began recommending claim outcomes, scoring fraud or setting reserves that adjusters rely on, TR-D would apply. Combined with TR-C, that makes the agent Critical, with [T3](tiering.md#t3) recommended.
- If draft-claim writes were auto-approved, that action class would be at [A3](tiering.md#a3). The agent would gain the AUTO tag and meet TR-B, adding [BAL-3.9](../controls/control-catalog.md#bal-3-9), [3.10](../controls/control-catalog.md#bal-3-10) and [3.11](../controls/control-catalog.md#bal-3-11) at [T2](tiering.md#t2) and [BAL-6.22](../controls/control-catalog.md#bal-6-22) at [T3](tiering.md#t3). The promotion would go through the [BAL-3.1](../controls/control-catalog.md#bal-3-1) gate, and [BAL-3.5](../controls/control-catalog.md#bal-3-5) would then need a deterministic constraint on each write, such as specified writes and targets pre-authorized with limits and expiry at the promotion gate, enforced outside the model, in place of per-write approval.

## Step 4: Applicable controls

Applicability comes from matching the five tags against each control's applies-to expression in the [control catalog](../controls/control-catalog.csv). A comma means OR and a plus sign means AND.

### Asset [T1](tiering.md#t1): 39 controls

| Control | Name | Matched clause |
|---|---|---|
| [BAL-1.4](../controls/control-catalog.md#bal-1-4) | Human owner of record | ALL |
| [BAL-1.5](../controls/control-catalog.md#bal-1-5) | AI asset risk rating and capability profile | ALL |
| [BAL-1.6](../controls/control-catalog.md#bal-1-6) | AI intake and registration gate | ALL |
| [BAL-1.7](../controls/control-catalog.md#bal-1-7) | AI bill of materials | BUILT |
| [BAL-1.12](../controls/control-catalog.md#bal-1-12) | Regulatory classification and governance hand-off | ALL |
| [BAL-1.15](../controls/control-catalog.md#bal-1-15) | AI asset decommissioning | ALL |
| [BAL-2.1](../controls/control-catalog.md#bal-2-1) | Scoped agent identity | AGENT |
| [BAL-2.2](../controls/control-catalog.md#bal-2-2) | Sponsored agent identity lifecycle | AGENT |
| [BAL-2.3](../controls/control-catalog.md#bal-2-3) | Attributable delegated actions | AGENT |
| [BAL-2.4](../controls/control-catalog.md#bal-2-4) | Agent credential storage, lifetime and revocation | AGENT, EXT |
| [BAL-2.8](../controls/control-catalog.md#bal-2-8) | MCP server authentication and token audience | EXT |
| [BAL-3.1](../controls/control-catalog.md#bal-3-1) | [Autonomy level](tiering.md#autonomy-levels) enforcement and promotion | AGENT |
| [BAL-3.2](../controls/control-catalog.md#bal-3-2) | Deterministic tool policy enforcement | BUILT+AGENT |
| [BAL-3.3](../controls/control-catalog.md#bal-3-3) | Capability-classified tool policy | BUILT+AGENT |
| [BAL-3.4](../controls/control-catalog.md#bal-3-4) | Audience-bound minimal scopes | AGENT |
| [BAL-3.5](../controls/control-catalog.md#bal-3-5) | Untrusted-input capability separation | UNTRUSTED |
| [BAL-3.6](../controls/control-catalog.md#bal-3-6) | Human approval of high-risk actions | ACT |
| [BAL-3.7](../controls/control-catalog.md#bal-3-7) | Agent kill switch | AGENT |
| [BAL-4.1](../controls/control-catalog.md#bal-4-1) | Data classification enforcement | ALL |
| [BAL-4.4](../controls/control-catalog.md#bal-4-4) | AI data retention and deletion | ALL |
| [BAL-4.6](../controls/control-catalog.md#bal-4-6) | Destination-aware input protection | ALL |
| [BAL-4.11](../controls/control-catalog.md#bal-4-11) | Output disclosure control | ALL |
| [BAL-5.1](../controls/control-catalog.md#bal-5-1) | AI threat modeling | BUILT+ACT, BUILT+UNTRUSTED |
| [BAL-5.2](../controls/control-catalog.md#bal-5-2) | AI change management | BUILT |
| [BAL-5.3](../controls/control-catalog.md#bal-5-3) | Adversarial security test suite | BUILT |
| [BAL-5.4](../controls/control-catalog.md#bal-5-4) | Indirect injection and exfiltration testing | BUILT+UNTRUSTED |
| [BAL-5.5](../controls/control-catalog.md#bal-5-5) | Regression testing on change | BUILT |
| [BAL-5.6](../controls/control-catalog.md#bal-5-6) | AI security release gate | BUILT |
| [BAL-6.1](../controls/control-catalog.md#bal-6-1) | Authority set outside the model | BUILT+AGENT |
| [BAL-6.2](../controls/control-catalog.md#bal-6-2) | Untrusted content labeling and normalization | BUILT+UNTRUSTED |
| [BAL-6.3](../controls/control-catalog.md#bal-6-3) | Output rendering exfiltration control | UNTRUSTED |
| [BAL-6.4](../controls/control-catalog.md#bal-6-4) | Prompt injection detection and response | BUILT |
| [BAL-6.5](../controls/control-catalog.md#bal-6-5) | Disclosure-safe hidden context | BUILT |
| [BAL-6.10](../controls/control-catalog.md#bal-6-10) | Safe handling of model output by interpreters | BUILT+AGENT |
| [BAL-6.12](../controls/control-catalog.md#bal-6-12) | Agent execution limits | AGENT |
| [BAL-6.14](../controls/control-catalog.md#bal-6-14) | Agent egress control | BUILT+AGENT |
| [BAL-7.1](../controls/control-catalog.md#bal-7-1) | Agent action audit log | AGENT |
| [BAL-7.2](../controls/control-catalog.md#bal-7-2) | Protected prompt and response logging | ALL |
| [BAL-8.13](../controls/control-catalog.md#bal-8-13) | AI provider fallback and exit | ALL |

### Asset [T1](tiering.md#t1) controls that do not apply: 11

| Control | Name | Needs |
|---|---|---|
| [BAL-4.7](../controls/control-catalog.md#bal-4-7) | Permission-aware retrieval | RAG+BUILT |
| [BAL-4.8](../controls/control-catalog.md#bal-4-8) | Grounding-scope oversharing remediation | RAG |
| [BAL-4.9](../controls/control-catalog.md#bal-4-9) | RAG source registration and trust labeling | RAG+BUILT |
| [BAL-4.10](../controls/control-catalog.md#bal-4-10) | Agent memory governance and integrity | MEM |
| [BAL-5.12](../controls/control-catalog.md#bal-5-12) | Model artifact intake scanning | MODEL |
| [BAL-5.13](../controls/control-catalog.md#bal-5-13) | Safe model loading | MODEL |
| [BAL-5.14](../controls/control-catalog.md#bal-5-14) | Model integrity verification | MODEL |
| [BAL-5.23](../controls/control-catalog.md#bal-5-23) | Isolation of event-triggered agents in CI/CD | CODE+UNTRUSTED |
| [BAL-6.13](../controls/control-catalog.md#bal-6-13) | Agent execution isolation | EXEC |
| [BAL-6.19](../controls/control-catalog.md#bal-6-19) | Self-hosted AI service exposure and hardening | INFRA (assessed on the MCP server and AI gateway platform assets) |
| [BAL-8.1](../controls/control-catalog.md#bal-8-1) | External model risk assessment | MODEL |

### Asset [T2](tiering.md#t2): 20 controls (required because the agent is High)

| Domain | Controls |
|---|---|
| 2 | [BAL-2.10](../controls/control-catalog.md#bal-2-10) No standing agent privilege |
| 3 | [BAL-3.13](../controls/control-catalog.md#bal-3-13) Out-of-band approval for critical actions |
| 4 | [BAL-4.14](../controls/control-catalog.md#bal-4-14) AI state recovery |
| 5 | [BAL-5.7](../controls/control-catalog.md#bal-5-7) Scheduled security re-evaluation; [BAL-5.8](../controls/control-catalog.md#bal-5-8) Multi-step agent testing; [BAL-5.9](../controls/control-catalog.md#bal-5-9) Adaptive prompt-injection testing; [BAL-5.10](../controls/control-catalog.md#bal-5-10) Drift and degradation detection; [BAL-5.11](../controls/control-catalog.md#bal-5-11) Guardrail efficacy measurement |
| 6 | [BAL-6.6](../controls/control-catalog.md#bal-6-6) Topic and intent policy; [BAL-6.7](../controls/control-catalog.md#bal-6-7) Input content and multimodal inspection; [BAL-6.8](../controls/control-catalog.md#bal-6-8) Harmful content filtering; [BAL-6.11](../controls/control-catalog.md#bal-6-11) Structured output validation; [BAL-6.15](../controls/control-catalog.md#bal-6-15) Tenant-restricted egress; [BAL-6.18](../controls/control-catalog.md#bal-6-18) Non-bypassable AI policy enforcement point |
| 7 | [BAL-7.5](../controls/control-catalog.md#bal-7-5) AI activity anomaly detection; [BAL-7.6](../controls/control-catalog.md#bal-7-6) Data concentration detection; [BAL-7.8](../controls/control-catalog.md#bal-7-8) Policy decision records; [BAL-7.9](../controls/control-catalog.md#bal-7-9) Investigation reconstruction; [BAL-7.10](../controls/control-catalog.md#bal-7-10) Hardened prompt log protection; [BAL-7.11](../controls/control-catalog.md#bal-7-11) Agentic action provenance |

Two of these need a note:

- **[BAL-3.13](../controls/control-catalog.md#bal-3-13)** applies (ACT), but the agent has no financial, permission-grant or irreversible production action class, so the control's condition does not arise. It is recorded as Implemented, with the [BAL-3.3](../controls/control-catalog.md#bal-3-3) capability classification as evidence, not as Not applicable.
- **[BAL-7.6](../controls/control-catalog.md#bal-7-6)** is tailored under exception EXAMPLE-EXC-001 (see step 6).

Thirteen asset [T2](tiering.md#t2) controls do not apply: [BAL-2.11](../controls/control-catalog.md#bal-2-11) (EXEC), [BAL-2.12](../controls/control-catalog.md#bal-2-12) and [6.21](../controls/control-catalog.md#bal-6-21) (MULTI), [BAL-3.9](../controls/control-catalog.md#bal-3-9) (AUTO, PUBLIC), [BAL-3.10](../controls/control-catalog.md#bal-3-10) and [3.11](../controls/control-catalog.md#bal-3-11) (AUTO), [BAL-4.2](../controls/control-catalog.md#bal-4-2) (RAG, MEM), [BAL-4.3](../controls/control-catalog.md#bal-4-3), [4.12](../controls/control-catalog.md#bal-4-12) and [6.9](../controls/control-catalog.md#bal-6-9) (BUILT+RAG), and [BAL-4.13](../controls/control-catalog.md#bal-4-13), [4.15](../controls/control-catalog.md#bal-4-15) and [5.15](../controls/control-catalog.md#bal-5-15) (MODEL).

### [T3](tiering.md#t3)

[BAL-2.13](../controls/control-catalog.md#bal-2-13) (sender-constrained agent tokens) matches the AGENT tag and is optional for a High asset. [BAL-4.16](../controls/control-catalog.md#bal-4-16) and [6.22](../controls/control-catalog.md#bal-6-22) do not apply.

### Program and Vendor controls this agent relies on

These are assessed once for the organization, not on this agent's rows:

- The 23 unconditional Program and Vendor [T1](tiering.md#t1) controls, with [BAL-8.2](../controls/control-catalog.md#bal-8-2) to [8.5](../controls/control-catalog.md#bal-8-5) assessed for the model provider's service and plan.
- [BAL-5.16](../controls/control-catalog.md#bal-5-16), [5.17](../controls/control-catalog.md#bal-5-17) and [5.18](../controls/control-catalog.md#bal-5-18), because the agent carries EXT: the two MCP servers are reviewed, pinned to their approved tool-definition fingerprints and listed in the approved component catalog.
- The Program and Vendor [T2](tiering.md#t2) controls that become required once a High asset carries their tags: [BAL-1.14](../controls/control-catalog.md#bal-1-14), [7.12](../controls/control-catalog.md#bal-7-12) and [8.11](../controls/control-catalog.md#bal-8-11) (ALL), [BAL-2.9](../controls/control-catalog.md#bal-2-9) (AGENT), [BAL-3.12](../controls/control-catalog.md#bal-3-12) (ACT) and [BAL-7.7](../controls/control-catalog.md#bal-7-7) (EXT). [BAL-8.6](../controls/control-catalog.md#bal-8-6) is recorded as Implemented with its condition absent: the model provider only serves the model through an API, and the organization operates the agent runtime, tool execution and rendering.

**Result: 59 Asset rows apply to this agent, 39 at [T1](tiering.md#t1) and 20 at [T2](tiering.md#t2), out of 128 controls.**

## Step 5: The main attack path and the controls that break it

**The attack (hypothetical).** An attacker submits a claim by email. The attached claim form carries hidden text, in white-on-white type and zero-width characters, that tells the agent to:

1. look up a list of other policy numbers (AML.T0053, AI Agent Tool Invocation);
2. copy the policyholders' details into the claim notes;
3. add a Markdown image whose address encodes those details and points at the attacker's server (AML.T0077, LLM Response Rendering);
4. file the draft against the attacker's own policy, so the details come back in later claim correspondence (AML.T0086, Exfiltration via AI Agent Tool Invocation).

This is an indirect prompt injection (AML.T0051.001; OWASP LLM01:2026 and ASI01) aimed at leaking other claimants' data (AML.T0057) or corrupting claim records. The controls below put into practice, among others, the ATLAS mitigations AML.M0030 (Restrict AI Agent Tool Invocation on Untrusted Data) and AML.M0029 (Human In-the-Loop for AI Agent Actions).

| # | Stage | Control | What it does on this path | One evidence item |
|---|---|---|---|---|
| 1 | Design | [BAL-3.5](../controls/control-catalog.md#bal-3-5) Untrusted-input capability separation | Leaves no unconstrained outbound channel in a session that holds untrusted email and claimant data. | Rule of Two profile in the asset register naming the constraint on each C channel, signed off at the rating review |
| 2 | Before release | [BAL-5.4](../controls/control-catalog.md#bal-5-4) Indirect injection and exfiltration testing | Shows the path fails before go-live, with injected instructions and canary exfiltration on every untrusted input path. | Release-gate report RG-2026-091: canary attempts through the message body, attachment text, image text and `policy_lookup` output all failed |
| 3 | Entry | [BAL-6.2](../controls/control-catalog.md#bal-6-2) Untrusted content labeling and normalization | Strips the hidden characters and active markup, and passes the email to the model only as labeled untrusted data. | Pre-processor configuration and test output for a seeded attachment, showing zero-width, bidirectional and tag characters removed |
| 4 | Entry | [BAL-6.4](../controls/control-catalog.md#bal-6-4) Prompt injection detection and response | Acts as a tripwire: a detected override attempt downgrades the session to no-write and sends the email to the manual queue. | Detection rule and response runbook, with a test event that reached the security operations queue |
| 5 | Authority | [BAL-6.1](../controls/control-catalog.md#bal-6-1) Authority set outside the model | Email text cannot add tools, widen scopes or change targets; the two tools and their scopes come from deployment configuration. | Test log showing an injected request to use an unlisted tool denied by the enforcement point |
| 6 | Collection | [BAL-3.2](../controls/control-catalog.md#bal-3-2) Deterministic tool policy enforcement | Checks each call against an allowlist keyed by server identity, tool name and definition fingerprint; `policy_lookup` accepts one well-formed policy number, and draft fields are schema-checked. | Enforcement-point policy file and a decision-log entry rejecting a multi-policy lookup |
| 7 | Collection | [BAL-6.12](../controls/control-catalog.md#bal-6-12) Agent execution limits | Caps each run at three lookups, 25 steps and five minutes. | Runtime limits configuration and a test run terminated at the lookup limit |
| 8 | Exit: rendering | [BAL-6.3](../controls/control-catalog.md#bal-6-3) Output rendering exfiltration control | The review screen does not fetch the attacker's image or unfurl links. | Rendering test with a canary image URL in model output: no request reached the canary host |
| 9 | Exit: network | [BAL-6.14](../controls/control-catalog.md#bal-6-14) Agent egress control | The runtime cannot reach any host outside the four-host allowlist, including through DNS. | Network policy and resolver configuration exports |
| 10 | Exit: writes | [BAL-3.6](../controls/control-catalog.md#bal-3-6) Human approval of high-risk actions | The adjuster sees the exact field values, with hidden characters revealed, before any write; altered or replayed approvals fail. | Approval screen specification and negative tests rejecting altered and replayed approvals |
| 11 | Respond | [BAL-7.1](../controls/control-catalog.md#bal-7-1) Agent action audit log | The enforcement point records every lookup and write with agent identity, approver, decision and rule, linked to the email. | Log sample tying the email ID, tool call, decision and approving adjuster together under one correlation ID |
| 12 | Respond | [BAL-3.7](../controls/control-catalog.md#bal-3-7) Agent kill switch | An operator can stop the agent, revoke its credentials and disable the mail trigger. | Kill-switch test record: halt completed within the 15-minute objective, queued runs canceled and the trigger disabled |

Other applicable controls do supporting work. Owner, rating and intake ([BAL-1.4](../controls/control-catalog.md#bal-1-4) to [1.6](../controls/control-catalog.md#bal-1-6)) make the decisions above someone's job. A scoped identity with minimal scopes ([BAL-2.1](../controls/control-catalog.md#bal-2-1), [BAL-3.4](../controls/control-catalog.md#bal-3-4)) limits what a hijacked run can reach. Destination-aware input protection ([BAL-4.6](../controls/control-catalog.md#bal-4-6)) keeps secrets and data classes not approved for the model out of the model call.

## Step 6: Example assessment rows

<a id="shared-identity-assessment"></a>
**Shared identity assessment (illustrative).** IAM-GOV-2026-Q3 assesses [BAL-2.2](../controls/control-catalog.md#bal-2-2) as Implemented for the program's enrolled agent identities, including EXAMPLE-AST-002. Its evidence, reviewed on 2026-09-10, records a named claims-operations sponsor, quarterly access certification for this High asset, and a tested sponsor-leaver workflow. This is the shared record linked by the Inherited (program) row below; a real assessment would link to the organization's retrievable assessment and evidence.

Five rows, showing selected columns of the [assessment template](assessment-template.csv) (the template also carries domain, control, [Control Tier](tiering.md#control-tiers), scope and applies_to):

```csv
control_id,asset_id,applicable,status,inherited_from,evidence,evidence_date,owner,target_date,exception_id,notes
BAL-3.5,EXAMPLE-AST-002,Y,Implemented,,"Rule of Two profile in the asset register naming the constraint on each C channel (writes approved under BAL-3.6; no remote rendering under BAL-6.3; egress allowlist under BAL-6.14); release-gate report RG-2026-091: canary exfiltration attempts failed on all four untrusted input paths",2026-09-22,Claims AI product owner,,,Re-verify when a tool or an input or output path is added (BAL-5.2)
BAL-3.6,EXAMPLE-AST-002,Y,Implemented,,"Approval screen specification: rendered by the claims system, every field value shown, hidden and confusable characters revealed; negative tests: altered and replayed approvals rejected; approver role limited to licensed adjusters",2026-09-22,Claims AI product owner,,,Draft-claim writes are the only A2 action class
BAL-6.14,EXAMPLE-AST-002,Y,Partially implemented,,"Network policy export: default-deny egress, four allowlisted hosts (AI gateway, two MCP servers, mail API), DNS only through the filtering resolver. Missing: a defined allowlist review cadence and monitoring for domain expiry and ownership change",2026-09-15,Platform security engineering lead,2026-11-30,,"Asset fails T1 conformance until closed; owner chose remediation over risk acceptance"
BAL-2.2,EXAMPLE-AST-002,Y,Inherited (program),PROGRAM,"Shared BAL-2.2 assessment: IAM-GOV-2026-Q3 (worked-example.md#shared-identity-assessment); assessment and evidence cover EXAMPLE-AST-002: identity enrolled with named sponsor (claims operations director), certified in Q3 2026, sponsor leaver trigger configured",2026-09-10,IAM governance lead,,,Quarterly certification because the asset is rated High
BAL-7.6,EXAMPLE-AST-002,Y,Excepted,,"Exception EXAMPLE-EXC-001; compensating controls evidenced in the BAL-3.2, BAL-6.12 and BAL-7.5 rows",2026-09-29,Claims AI product owner,,EXAMPLE-EXC-001,"T2 tailoring: in-session aggregation is bounded deterministically; reported as tailored, not covered"
```

What each row shows:

- **[BAL-3.5](../controls/control-catalog.md#bal-3-5), Implemented.** The evidence is the recorded decision plus the test that proves it, not a design document alone.
- **[BAL-3.6](../controls/control-catalog.md#bal-3-6), Implemented.** The approval is rendered by the enforcement point (here the claims system), not summarized by the model, and the negative tests show that approvals cannot be altered or reused.
- **[BAL-6.14](../controls/control-catalog.md#bal-6-14), Partially implemented.** Enforcement is in place, but two sub-requirements are not: a defined review cadence for the allowlist, and monitoring of allowlisted domains for expiry and ownership change. A control is Implemented only when every sub-requirement is met. The owner chose to remediate by the target date rather than request a risk acceptance, so until then the agent fails asset [T1](tiering.md#t1) conformance and is counted as a fail in the High row of that metric.
- **[BAL-2.2](../controls/control-catalog.md#bal-2-2), Inherited (program).** Identity governance for non-human identities is a program-wide process. The row points to [shared assessment IAM-GOV-2026-Q3](#shared-identity-assessment) and evidence that this agent's identity is enrolled, sponsored and certified at the cadence its rating requires. In a real assessment, replace that illustrative pointer with the retrievable record in the organization's evidence repository. A gap or stale evidence in that assessment would also be a gap for this agent.
- **[BAL-7.6](../controls/control-catalog.md#bal-7-6), Excepted.** The specific risk, aggregation of sensitive data within a session, is bounded deterministically by [BAL-3.2](../controls/control-catalog.md#bal-3-2) and [BAL-6.12](../controls/control-catalog.md#bal-6-12), and cross-session volume is watched by [BAL-7.5](../controls/control-catalog.md#bal-7-5). The tailoring is approved by a CISO delegate, whose authority matches a High asset, and expires after 12 months. It is reported as tailored and never counts as covered.

**Result.** If every other row is covered, this assessment reports the agent as failing asset [T1](tiering.md#t1) conformance (one Partially implemented row, [BAL-6.14](../controls/control-catalog.md#bal-6-14)) and as "pass with tailoring" for [T2](tiering.md#t2) conformance (one Excepted row). The organization can include the agent in a [T1](tiering.md#t1) conformance claim only after [BAL-6.14](../controls/control-catalog.md#bal-6-14) is closed with fresh evidence.

Back to the [adoption guide](adoption.md) or the [framework overview](../README.md).
