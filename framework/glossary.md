# Glossary

Terminology employed throughout the Ballast controls, guides, and templates. When a term denotes a capability tag, the tag is displayed in uppercase; tags, [Control Tiers](../guides/tiering.md#control-tiers), and the risk rubric are detailed in [Control Tiers](../guides/tiering.md).

### Action class

A group of actions an AI asset can take that share an impact, for which an [autonomy level](../guides/tiering.md#autonomy-levels) ([A0](../guides/tiering.md#a0)-[A4](../guides/tiering.md#a4)) is recorded and enforced ([BAL-1.5](../controls/control-catalog.md#bal-1-5), [BAL-3.1](../controls/control-catalog.md#bal-3-1)). Each asset records its action classes in the asset register: its read classes, the [BAL-3.3](../controls/control-catalog.md#bal-3-3) capability classes it can use (filesystem write, network egress, credential access, code execution, destructive, financial, identity or permission change, publishing, external communication), and the [BAL-3.6](../controls/control-catalog.md#bal-3-6) high-risk classes among them. For a vendor-operated asset, which has no [BAL-3.3](../controls/control-catalog.md#bal-3-3) classification, the action classes are the actions the vendor's service exposes, grouped the same way. One agent can be [A3](../guides/tiering.md#a3) for updating ticket fields and [A2](../guides/tiering.md#a2) for sending external email.

### Agent

An AI application capable of invoking tools, functions, connectors, or APIs, and determining which to invoke along with the appropriate arguments to accomplish a task (AGENT tag). An agent operates as an identity within the Domain 2, and its degree of [autonomy](../guides/tiering.md#autonomy-levels) is configured on a per-action class basis. Even if an agent's action classes are all designated as [A0](../guides/tiering.md#a0), it remains classified as an agent.

### AI application

Software employing one or more models to execute a task for individuals or other systems, including examples like a chat assistant, summarizer, classifier, or retrieval-augmented service. Assistants and agents constitute specific instances of AI application.

### AI asset

The Ballast unit registers, rates, and assesses: an AI application, assistant, agent, model, AI feature enabled in a SaaS product, AI coding tool, or self-hosted AI service. Every asset possesses an owner ([BAL-1.4](../controls/control-catalog.md#bal-1-4)), a risk rating, and capability tags ([BAL-1.5](../controls/control-catalog.md#bal-1-5)), and is registered prior to reaching production users or data ([BAL-1.6](../controls/control-catalog.md#bal-1-6)). Pilots and developer tools that interact with real data constitute AI assets.

### AI BOM (AI bill of materials)

The record, for each AI application and agent the organization builds or configures, of its models and versions, agents, skills and plugins, MCP servers and tools, retrieval sources and indexes, and owners, kept current at each release or material change ([BAL-1.7](../controls/control-catalog.md#bal-1-7)). [CycloneDX ML-BOM](https://cyclonedx.org/capabilities/mlbom/) and the [SPDX 3.0 AI profile](https://spdx.github.io/spdx-spec/v3.0.1/) are example formats.

### Applies-to tag

A capability label drawn from Ballast's fixed vocabulary of 17 tags (for instance, AGENT, RAG, EXEC, UNTRUSTED). Every asset logs its tags under [BAL-1.5](../controls/control-catalog.md#bal-1-5), and each control features an applies-to expression where a comma denotes OR and a plus sign indicates AND. A control is applicable when the asset's tags meet the criteria set by its expression.

### Assistant

An AI application that responds to a person in an interactive session by answering, drafting or summarizing, without calling tools itself. Retrieval or grounding on enterprise content alone does not make an assistant an agent; once it can call tools, functions, connectors or APIs, it is an agent.

### Autonomy level ([A0](../guides/tiering.md#a0)-[A4](../guides/tiering.md#a4))

How far an agent may act without a person, recorded per action class and enforced outside the model ([BAL-3.1](../controls/control-catalog.md#bal-3-1)). An asset's agency is its highest level across action classes.

| Level | Name | Meaning |
|---|---|---|
| [A0](../guides/tiering.md#a0) | Read-only | No state-changing tools. Rendering links or images, fetching URLs and writing memory are still outbound channels ([BAL-3.5](../controls/control-catalog.md#bal-3-5), [BAL-6.3](../controls/control-catalog.md#bal-6-3)). |
| [A1](../guides/tiering.md#a1) | Suggest | Proposes content or actions that a human carries out through a separate, normal channel. One-click execution of a proposed tool call is [A2](../guides/tiering.md#a2). |
| [A2](../guides/tiering.md#a2) | Act with approval | Executes after per-action human approval rendered by the enforcement point ([BAL-3.6](../controls/control-catalog.md#bal-3-6)). If auto-approve is enabled for an action class, that class is [A3](../guides/tiering.md#a3). |
| [A3](../guides/tiering.md#a3) | Bounded autonomous | Acts without per-action approval inside a declared envelope of tools, scopes, egress, rate, budget and time. High-risk actions need per-action approval unless an authorized person approves specified actions and targets within recorded limits and an expiry date at the promotion gate. Limits are enforced outside the model; other required reviews still apply. |
| [A4](../guides/tiering.md#a4) | [High autonomy](../guides/tiering.md#autonomy-levels) | Self-initiated or open-ended goals. Allowed only with an [A4](../guides/tiering.md#a4) authorization ([BAL-1.13](../controls/control-catalog.md#bal-1-13)) approved by an executive risk owner, with all applicable [T2](../guides/tiering.md#t2) and [T3](../guides/tiering.md#t3) controls. Prohibited for consequential decisions about individuals, restricted data, irreversible financial actions, and assets that do not meet [BAL-3.5](../controls/control-catalog.md#bal-3-5). |

### Consequential decision

A decision with a legal or similarly significant effect on an individual, such as access to, or the terms of, employment, credit, insurance (including underwriting, pricing and claims), housing, education, healthcare or essential services. An asset materially supports such a decision when its output is a substantial factor in it, for example by scoring, ranking, recommending or flagging the individual, even if a person makes the final call; transcribing or routing information alone does not. Recorded under [BAL-1.12](../controls/control-catalog.md#bal-1-12); it drives rule TR-D, and [A4](../guides/tiering.md#a4) is prohibited for such assets.

### Detected

A detection requirement is met only when an alert reaches an accountable owner and is handled under a defined response. A log entry or dashboard that nobody acts on does not count. This definition applies to every control that uses the word.

### Enforcement point

A deterministic component outside the model that applies policy to the model's inputs, outputs or actions: for example an AI gateway, tool or MCP proxy, SDK middleware, sandbox, egress proxy, identity provider or platform control. The model cannot change its configuration. Tool policy ([BAL-3.2](../controls/control-catalog.md#bal-3-2)), approval prompts ([BAL-3.6](../controls/control-catalog.md#bal-3-6)) and action records ([BAL-7.1](../controls/control-catalog.md#bal-7-1)) come from the enforcement point, not from the model. A prompt instruction is not an enforcement point. SDK middleware alone cannot meet the non-bypassable boundary required by [BAL-6.18](../controls/control-catalog.md#bal-6-18).

### Exception, tailoring, risk acceptance and [A4](../guides/tiering.md#a4) authorization

An **exception** is a recorded departure from an applicable control. The [BAL-1.13](../controls/control-catalog.md#bal-1-13) register holds two kinds of control exception and a separate authorization decision:

- **Tailoring**: a [T2](../guides/tiering.md#t2) control is replaced by a documented compensating control that addresses the same risk, for at most 12 months. Renew only with fresh approval and current evidence for the compensating control.
- **Risk acceptance**: an applicable control (typically [T1](../guides/tiering.md#t1)) is not met and the residual risk is accepted by an approver whose authority scales with the asset's risk rating, for at most 6 months for High or Critical assets and 12 months otherwise, with one renewal only under a funded remediation plan. It always counts as a gap.

- **[A4](../guides/tiering.md#a4) authorization**: permission from an executive risk owner to operate at [A4](../guides/tiering.md#a4) while all required controls are met, for at most 6 months. Every renewal needs a new [BAL-3.1](../controls/control-catalog.md#bal-3-1) promotion gate. It does not make a satisfied control Excepted.

Expired tailoring and risk acceptances revert to open gaps. [A4](../guides/tiering.md#a4) operation must stop when its authorization expires. Not applicable is not an exception, and the non-acceptable controls listed in [Control Tiers](../guides/tiering.md#non-acceptable-controls) cannot be excepted (the only route is the narrow one [BAL-1.6](../controls/control-catalog.md#bal-1-6) gives vendor-enabled features that cannot be held off).

### EXEC

EXEC covers code, shell commands and model-directed filesystem writes. A data-only export through an application that controls the destination, format and recipient permissions does not add EXEC by itself, provided it cannot write executable content or configuration files. The export remains a state-changing action. Ordinary file reads alone do not add EXEC.

### High-risk action

An action in one of the [BAL-3.6](../controls/control-catalog.md#bal-3-6) classes: payments and financial commitments; transfer of data outside the trust boundary or to recipients not already entitled to it; secret retrieval or privileged credential use; external communications; destructive or irreversible operations; production changes, including merges to protected branches, releases and deployments; permission, access, credential or account-recovery changes; changes to security controls or monitoring, including closing or suppressing alerts; installing dependencies, extensions or MCP servers not already approved; and publishing to shared, public or personal destinations. Each needs per-action approval by an authorized person unless that person approves specified actions and targets within recorded limits and an expiry date at an [A3](../guides/tiering.md#a3) promotion gate. Limits are enforced outside the model; other required human reviews still apply. The [BAL-3.13](../controls/control-catalog.md#bal-3-13) classes use a separate approval channel for approval, changes and renewals.

### Inherited

An Asset control is Inherited (program), Inherited (platform) or Inherited (vendor) only while a linked shared assessment and current evidence show it is met for that asset. Name the provider in inherited_from. A gap or stale evidence in the shared control is a gap for dependent assets; tailoring or risk acceptance must explicitly cover those assets and their risk ratings. Count each asset's required control once, without counting shared-evidence records as extra assets or coverage. Program and Vendor controls count once in their own scopes.

### Initiation mode

How a run of an agent starts: human-initiated (a person invokes it) or event-triggered (a schedule, webhook, inbound message or other event). It is recorded with the [autonomy levels](../guides/tiering.md#autonomy-levels) ([BAL-1.5](../controls/control-catalog.md#bal-1-5), [BAL-3.1](../controls/control-catalog.md#bal-3-1)). A run triggered by external content, such as an inbound email, counts as processing untrusted content. A scheduled task limited to ordinary reads remains [A0](../guides/tiering.md#a0). Choosing its own goals or starting work without a human-defined task remains subject to [A4](../guides/tiering.md#a4). Secret retrieval, privileged credential use and outbound actions keep their existing approval requirements.

### Material change

A modification capable of affecting an asset's risk profile: a revised model or model version, encompassing a provider-driven update or redirection of alias; an updated tool, action class, MCP server or connector; a distinct data source or elevated data classification; an expanded user demographic, incorporating external participants; a shift in [autonomy level](../guides/tiering.md#autonomy-levels) or initiation mechanism; or any alteration introducing a capability tag. Such a material change necessitates re-registration ([BAL-1.6](../controls/control-catalog.md#bal-1-6)), re-rating ([BAL-1.5](../controls/control-catalog.md#bal-1-5)), and change management ([BAL-5.2](../controls/control-catalog.md#bal-5-2)).

### MCP server

A server that implements the Model Context Protocol and exposes tools, resources or prompts to AI clients such as agents, assistants and IDEs. A local server is launched by the client on the same machine, usually over stdio; a remote server is reached over HTTP. Using one tags an asset EXT; operating one is INFRA. Its tool output is untrusted content, and its tool definitions are reviewed and fingerprinted before use ([BAL-5.16](../controls/control-catalog.md#bal-5-16), [BAL-5.17](../controls/control-catalog.md#bal-5-17)).

### Not applicable

The status of a control whose applies-to expression the asset's tags do not satisfy. It is derived from tags, never chosen, and needs no approval. A control whose enforcement point sits inside a vendor's service is not Not applicable for that reason. Where a tagged control states a condition that does not arise (for example [BAL-3.13](../controls/control-catalog.md#bal-3-13) for an asset with no financial actions), record Implemented with evidence that the condition is absent; see the conditional-requirements rule in the [tiering guide](../guides/tiering.md#applies-to-tags).

### Pilot

Time-limited, pre-production use of an AI asset with real (non-synthetic) organizational data, real identities or credentials, or real users, including proofs of concept and trials of developer tools. A pilot is in [Control Tier](../guides/tiering.md#control-tiers) scope: it meets the pilot minimum before first real use, and full applicable [T1](../guides/tiering.md#t1) at production release or 90 days after first real-data use, whichever comes first. A sandbox that uses only synthetic data, with no real identities, credentials or users, is not a pilot.

### Production

Use of an AI asset by its intended users for ongoing business purposes. A pilot is treated as production from 90 days after its first use of real data.

### Promotion gate

The recorded decision, under [BAL-3.1](../controls/control-catalog.md#bal-3-1), that raises an action class to a higher [autonomy level](../guides/tiering.md#autonomy-levels) or deploys an agent with any action class above [A2](../guides/tiering.md#a2). It requires evidence that the controls required at the target level, as set by the re-assessed risk rating, are implemented and tested; an operating record at a lower level for a defined minimum period (for a new agent, from a pilot at [A2](../guides/tiering.md#a2) or below); and owner and security sign-off under [BAL-1.2](../controls/control-catalog.md#bal-1-2). Any [A3](../guides/tiering.md#a3) pre-authorization records the approved actions, targets, limits and expiry here; the system enforces them outside the model and retains other required reviews. Link an [A4](../guides/tiering.md#a4) authorization from the [BAL-3.1](../controls/control-catalog.md#bal-3-1) assessment using its existing evidence, notes and exception_id fields. An agent identity cannot change its own level, tools, scopes or approval settings, or create agents, triggers or schedules at a higher level than its own.

### Provider-implemented (evidenced)

The status of a control whose enforcement point sits inside a vendor-operated service. It counts toward coverage only with evidence specific to the control: vendor documentation mapped to the control, an independent attestation whose scope covers the feature in use, or the organization's own test. The evidence is gathered through the tenant configuration baseline ([BAL-6.17](../controls/control-catalog.md#bal-6-17)) and, for High and Critical assets tagged UNTRUSTED or ACT whose runtime or rendering the vendor operates, the vendor-hosted security review ([BAL-8.6](../controls/control-catalog.md#bal-8-6)). It is reported separately from controls the organization implements itself.

### Risk rating

The Low, Medium, High or Critical rating each AI asset receives under [BAL-1.5](../controls/control-catalog.md#bal-1-5), using rules TR-A to TR-D. It sets the required [Control Tiers](../guides/tiering.md#control-tiers) (Low or Medium: [T1](../guides/tiering.md#t1); High: [T1](../guides/tiering.md#t1) and [T2](../guides/tiering.md#t2); Critical: [T1](../guides/tiering.md#t1) and [T2](../guides/tiering.md#t2), with [T3](../guides/tiering.md#t3) recommended and required at [A4](../guides/tiering.md#a4)), the approval workflow, the authority needed to approve exceptions and the review cadence. Use "risk rating" for assets, "[Control Tier](../guides/tiering.md#control-tiers)" for controls, and "plan" or "edition" for vendor offerings.

### Rule of Two

The design rule, from Meta's "[Agents Rule of Two](https://ai.meta.com/blog/practical-ai-agent-security/)" (October 2025), that within one session an agent should hold no more than two of: (A) untrusted input, (B) access to sensitive data or systems, and (C) the ability to change state or communicate externally. [BAL-3.5](../controls/control-catalog.md#bal-3-5) implements it. Ballast counts rendered links and images, URL fetches and memory writes as (C), and allows all three together only when each (C) action is constrained by a deterministic control, approved under [BAL-3.6](../controls/control-catalog.md#bal-3-6), or the workflow is split. Related: the "[lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)" (S. Willison, 2025) and [MITRE ATLAS](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.09) mitigation AML.M0030.

### Scope (Program, Vendor, Asset)

Where a control is implemented and assessed:

- **Program**: once, by the organization's AI security program; every asset inherits it.
- **Vendor**: once per AI vendor, service and plan; every asset that uses that service inherits it.
- **Asset**: for each in-scope AI asset, or once by an organization-wide platform, with each onboarded asset recording "Inherited (platform)".

### Sensitive data and restricted data

**Sensitive data** is any data the organization's classification scheme protects above public release, such as internal, confidential and client-confidential data, together with the systems that hold it. Property (B) of [BAL-3.5](../controls/control-catalog.md#bal-3-5) and rule TR-C refer to sensitive data. **Restricted data** is the highest classes in that scheme: regulated data (for example health, payment card and special-category personal data), credentials and secrets, and privileged systems. Rule TR-A, the [BAL-8.2](../controls/control-catalog.md#bal-8-2) non-acceptable condition and the [A4](../guides/tiering.md#a4) prohibitions refer to restricted data. Ballast does not define the classes; the organization's scheme does.

<a id="tier"></a>

### Control Tier

When a control is required: **[T1](../guides/tiering.md#t1) Baseline** for every in-scope asset and organization, **[T2](../guides/tiering.md#t2) Elevated risk** for assets rated High or Critical, and **[T3](../guides/tiering.md#t3) Advanced** for assets with an action class at [A4](../guides/tiering.md#a4) (recommended for Critical assets). [Control Tiers](../guides/tiering.md#control-tiers) are cumulative.

### Tool definition fingerprint

A content hash of the name, description and input schema of each tool a server presents, recorded when the server is approved ([BAL-5.17](../controls/control-catalog.md#bal-5-17)). Tool allowlists are keyed on the authenticated server identity, the tool name and the approved fingerprint ([BAL-3.2](../controls/control-catalog.md#bal-3-2)). A changed fingerprint blocks the tool until it is re-reviewed, which counters silent definition changes (AML.T0109, AI Supply Chain Rug Pull). A remote server can change its behavior without changing its definitions, so fingerprinting is paired with egress control ([BAL-6.14](../controls/control-catalog.md#bal-6-14)).

### Trust boundary

The edge of the systems, tenants, accounts and recipients that the organization controls and has authorized for the data in question. Data that crosses it, to an external party, a destination that is not allowlisted, a personal account or a recipient not already entitled to it, has left the organization's control: that is an outbound channel under [BAL-3.5](../controls/control-catalog.md#bal-3-5) and a high-risk action under [BAL-3.6](../controls/control-catalog.md#bal-3-6). In threat models ([BAL-5.1](../controls/control-catalog.md#bal-5-1)), trust boundaries also separate components that hold different levels of trust, such as the model and the tool enforcement point.

### Untrusted content

Content not authored by the organization or by the user invoking the asset: email, web pages, shared or uploaded files, tickets, tool and MCP output, and messages from other agents. Internal content that people outside a source's approved writer set can edit is also untrusted ([BAL-4.9](../controls/control-catalog.md#bal-4-9)). Untrusted content enters context as labeled data ([BAL-6.2](../controls/control-catalog.md#bal-6-2)), and because authority is set outside the model, it cannot add tools, widen scopes or change recipients ([BAL-6.1](../controls/control-catalog.md#bal-6-1)). An asset that processes it carries the UNTRUSTED tag.

Back to the [framework overview](../README.md).
