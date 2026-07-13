# Architecture — MailReader

## Project #24 preservation profile

Source of truth: `docs/ARCHITECTURE.yaml`. Tracking issue: https://github.com/googa27/MailReader/issues/1. Profile: `legacy`; enforcement: Advisory.

This repository is preserved as `Legacy Skeleton`. The governance files are intentionally advisory and additive: they document provenance, risks, and revival gates without refactoring inherited code or claiming active maintenance.

## Archival, supersession, and provenance

- Archival notice: historical/reference preservation only; not production-ready, maintained, secure, or operationally validated.
- Supersession notice: prefer upstream or maintained libraries for new work.
- Canonical/provenance: near-empty legacy repository owned by googa27; no upstream remote configured locally
- Upstream: No upstream remote is configured locally.
- License/provenance warning: Root LICENSE is MIT.
- Security/private-data warning: Email parsing touches untrusted content; isolate attachments, avoid remote fetching, and use least-privilege credentials/keyrings on revival. Never commit mailboxes, message bodies, addresses, credentials, OAuth tokens, app passwords, exports, or CSVs derived from private email.

## Research-backed defaults

| Decision | Evidence | Repository application |
|---|---|---|
| Agent context | Hermes context files; AGENTS.md convention | Root `AGENTS.md`; progressive detail in this architecture document. |
| AI tool escalation | MCP tools specification | Stable local contracts first; no repo-specific plugin/MCP during preservation. |
| Python source layout | PyPA src-layout guidance | No forced migration for legacy/fork/hardware preservation. |
| Test layout | pytest good practices | Unit/integration/e2e/architecture directories exist; empty suites declare activation triggers. |
| Module budget | Pylint too-many-lines rationale plus AI review locality | 500-line default is a no-growth ratchet where runtime source roots are activated. |
| Evolution | Evolutionary architecture | Revival requires executable fitness functions and explicit exceptions. |
| Data layers | Medallion architecture | Applied only if revived with real data; current posture is advisory. |
| Python protocols | Python data model; NumPy dispatch | Dunders are not decoration; API/protocol redesign waits for revival. |

## Maintained-library decision table

| Capability | Selected route | Alternatives | Boundary / custom-code rule |
|---|---|---|---|
| email parsing | Python stdlib email/mailbox/imaplib plus maintained parsers only if needed | Custom MIME/parser implementation | Keep parsing behind a typed, testable message-evidence boundary. |
| tabular export | pandas or csv stdlib based on scale | Ad hoc string concatenation | Exports must have redaction and schema tests before use. |
| credential storage | OS keyring/OAuth libraries after review | Plaintext passwords/tokens | No credentials in repo, logs, fixtures, or examples. |
| architecture bootstrap | Python standard-library json over JSON-subset YAML | Hand-written YAML parser | Dependency-free advisory gate only. |

## Data, security, and privacy posture

No current data architecture; any revival requires private-email classification, retention, redaction, and local-custody plan.

Never commit mailboxes, message bodies, addresses, credentials, OAuth tokens, app passwords, exports, or CSVs derived from private email.

Email parsing touches untrusted content; isolate attachments, avoid remote fetching, and use least-privilege credentials/keyrings on revival.

## AI and human interface

- AI interface: Minimal AGENTS explaining current skeleton and revival gate; no MCP/plugin.
- Human/notebook interface: No stable API yet; typed message/evidence interfaces only on revival.
- Core posture: Avoid core dependencies.

## Revival gates

- Define threat model, private-data classification, retention policy, and redaction rules before reading real mail.
- Use least-privilege OAuth/app credentials stored outside the repo; add secret scanning to CI before use.
- Create public-synthetic email fixtures and parser/export oracle tests.
- Declare supported providers/protocols and failure modes before stable API claims.

## Research anchors

- https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files
- https://agents.md/
- https://modelcontextprotocol.io/specification/2025-06-18/server/tools
- https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/
- https://docs.pytest.org/en/stable/explanation/goodpractices.html
- https://docs.python.org/3/reference/datamodel.html
- https://numpy.org/doc/stable/user/basics.dispatch.html
- https://evolutionaryarchitecture.com/precis.html
- https://learn.microsoft.com/en-us/azure/databricks/lakehouse/medallion
