## Project #24 Preservation notice

Status: **Legacy Prototype — Archived Source** (`legacy` profile, Advisory enforcement). This repository preserves a 2022 Gmail-to-settlement prototype for historical reference. It has no supported install, active application, certified runtime, or operational acceptance.

The original `master` history ends at `3658fddcd5e796b9bcb2b8a9231aa3db64bfd2ec`. Its complete tip tree is preserved byte-for-byte under [legacy/2022-mailreader](legacy/2022-mailreader/README.md); the manifest maps every original path and Git blob. The current governance history and the original history must both remain reachable after integration.

Root LICENSE is MIT. The original commits are attributed to the same repository owner, `googa27`; no upstream is configured.

**Privacy:** Never run the historical demo against real Gmail or commit mail, message bodies, addresses, credentials, OAuth tokens, exports, or private purchase records. Historical code writes tokens inside its source tree and logs parsed content. Ignore rules are a guard against accidental commits, not secure credential storage.

### Current contents and limitations

The archive contains Gmail acquisition, HTML receipt parsing, account aggregation and XLSX settlement scripts, plus inherited project metadata. Earlier default-branch descriptions that called this repository an implementation-free skeleton omitted the unrelated `master` history.

The prototype remains inactive: no runtime dependencies, wrapper, supported entrypoint, live account access, or new inference capability is introduced. Known defects include missing Gmail pagination, same-day order loss, first-run settlement failure, brittle MIME/date parsing, private-content logging and repository-local token storage. See the [archive notice](legacy/2022-mailreader/README.md) and [architecture contract](docs/ARCHITECTURE.yaml).

### Offline preservation checks

```bash
PYTHONDONTWRITEBYTECODE=1 python scripts/check_legacy_preservation.py
PYTHONDONTWRITEBYTECODE=1 python scripts/check_portfolio_architecture.py
PYTHONDONTWRITEBYTECODE=1 python scripts/check_ai_hierarchy_policy.py
PYTHONDONTWRITEBYTECODE=1 python scripts/selftest_ai_hierarchy_policy.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider tests/architecture
```

These checks inspect bytes, syntax and governance. They do not import or execute the archived source and do not prove runtime behavior.

### Revival gates

- Define a threat model, private-data classification, retention, redaction and local-custody policy before reading real mail.
- Keep least-privilege OAuth credentials in a reviewed platform credential store outside the repository.
- Select and pin maintained Google API, MIME/HTML parsing and tabular export libraries; use only public synthetic fixtures for verification.
- Repair the documented acquisition, parsing, aggregation and output defects; declare supported providers, setup, failure modes and test oracles before claiming a stable API.

See [AGENTS.md](AGENTS.md) and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

