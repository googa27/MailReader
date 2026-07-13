## Project #24 Preservation notice

Status: Legacy Skeleton (`legacy` profile, Advisory enforcement). This repository is preserved for historical/reference value and is not presented as maintained, production-ready, secure, or suitable for new operational use.

Supersession: prefer the canonical upstream or maintained libraries for new work. Canonical/provenance note: near-empty legacy repository owned by googa27; no upstream remote configured locally. Upstream: No upstream remote is configured locally.

License/provenance: Root LICENSE is MIT.

Security/private-data warning: Email parsing touches untrusted content; isolate attachments, avoid remote fetching, and use least-privilege credentials/keyrings on revival. Never commit mailboxes, message bodies, addresses, credentials, OAuth tokens, app passwords, exports, or CSVs derived from private email.

Revival gates:
- Define threat model, private-data classification, retention policy, and redaction rules before reading real mail.
- Use least-privilege OAuth/app credentials stored outside the repo; add secret scanning to CI before use.
- Create public-synthetic email fixtures and parser/export oracle tests.
- Declare supported providers/protocols and failure modes before stable API claims.

See `AGENTS.md` and `docs/ARCHITECTURE.yaml` for the advisory preservation contract.

---

# MailReader
Reading mails into CSV
