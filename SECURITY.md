# Security Policy

Ballast is a control framework published as documents and data files, not software. Its "security issues" are mostly problems in the guidance itself. Some of these should not be discussed in public until they are fixed.

## Report privately

Send a private LinkedIn message to [Raoul Hira](https://www.linkedin.com/in/raoulhira) or [Avishkar (Avi) Nikum](https://www.linkedin.com/in/avinikum) instead of opening a public issue when it concerns, for example:

- **Unsafe guidance:** a control, evidence example or guide that would weaken security if followed as written, or that gives false assurance about a risk it does not address.
- **Harmful references:** a link, mapping or cited resource that points to malicious, compromised or re-registered content.
- **Sensitive content in the repository:** credentials, personal data or confidential information that was committed by mistake.
- **Exploitable detail:** a gap whose public description would help attackers more than defenders, for example an attack pattern that bypasses a control and is not yet publicly known.

Please include the affected file and control ID, what is wrong, why it matters, and a suggested fix if you have one. Do not include real secrets, personal data or your organization's confidential information in the report.

## Report publicly

Open a normal issue, as described in [CONTRIBUTING.md](CONTRIBUTING.md), for unclear wording, coverage gaps, mapping corrections and anything else that does not need to stay private.

## Out of scope

Ballast does not run a bug bounty and cannot triage vulnerabilities in third-party AI products or services. Report those to the vendor concerned. If such a vulnerability shows that a Ballast control is missing or wrong, you are welcome to report that here once the vendor's disclosure process allows.

## What to expect

Ballast is maintained by its two authors, so responses are on a best-effort basis. The aim is to acknowledge a report within 5 business days, agree on a fix and timing with you, and credit you in the changelog if you wish. Fixes to unsafe guidance are released as soon as practical, and the changelog records the change without exploitable detail.

## Supported versions

Reports are handled against the latest release. At present that is 1.0.0.
