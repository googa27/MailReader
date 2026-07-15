# AGENTS.md — MailReader

Purpose: Project #24 legacy preservation. This repository is classified as `Legacy Skeleton` with `legacy` profile and Advisory enforcement. Do not make unsupported maturity, security, maintenance, or production-readiness claims.

Canonical docs:
- `README.md` root preservation notice
- `docs/ARCHITECTURE.yaml` machine-readable source of truth
- `docs/ARCHITECTURE.md` rationale and maintained-library/revival notes

Provenance and attribution:
- Origin owner: `googa27`; issue: https://github.com/googa27/MailReader/issues/1
- Upstream/canonical reference: none configured locally
- Preserve history, existing public names, authorship, copyright notices, and file contents. Do not delete, rewrite, or hide inherited material in this preservation change.

Safety boundaries:
- License/provenance: Root LICENSE is MIT.
- Data posture: No current data architecture; any revival requires private-email classification, retention, redaction, and local-custody plan.
- Private-data rule: Never commit mailboxes, message bodies, addresses, credentials, OAuth tokens, app passwords, exports, or CSVs derived from private email.
- Security/hardware warning: Email parsing touches untrusted content; isolate attachments, avoid remote fetching, and use least-privilege credentials/keyrings on revival.

Exact commands:
- Setup: no supported automated setup is declared; treating runtime setup as a revival gate is required.
- Tests: no inherited runtime test suite is claimed; run the architecture checker only.
- Lint/format: no lint/format command is declared.
- Architecture: `python scripts/check_portfolio_architecture.py`

Implementation rules for future work:
- Research upstream/current maintained libraries, standards, datasets, licenses, and security posture before changing runtime code.
- Prefer maintained libraries; custom code must be limited to domain semantics, adapters, composition, or genuinely missing algorithms with oracle/reference tests.
- Avoid invasive refactors of inherited code. Record exact no-growth exceptions and compatibility risks before structural changes.
- Do not introduce generated caches, secrets, private identifiers, restricted data, or fabricated outputs.
- Keep AI-facing contracts deterministic and local. Add Hermes skills for recurring workflows only; plugin/MCP needs stable public contracts, measured multi-client need, least privilege, and separate verification.
- Human/notebook interface: No stable API yet; typed message/evidence interfaces only on revival.
- Core posture: Avoid core dependencies.

Revival gates:
- Define threat model, private-data classification, retention policy, and redaction rules before reading real mail.
- Use least-privilege OAuth/app credentials stored outside the repo; add secret scanning to CI before use.
- Create public-synthetic email fixtures and parser/export oracle tests.
- Declare supported providers/protocols and failure modes before stable API claims.

Definition of done for preservation edits:
- README, AGENTS, `docs/ARCHITECTURE.yaml`, `docs/ARCHITECTURE.md`, and tests agree.
- `python scripts/check_portfolio_architecture.py` passes.
- Only advisory governance files are changed unless a separate reviewed revival task authorizes runtime edits.

### AI-assisted change controls

- Treat agent output as untrusted until a human reviews it and executable repository gates verify it. The human author remains accountable.
- Keep agent changes small, single-purpose, and completely reviewable. Generated tests are not a sufficient sole oracle for generated implementation.
- New dependencies require human approval plus package-existence, maintenance, API, license, vulnerability, and typosquat checks; lock reproducibly.
- Security-sensitive code (authentication, cryptography, parsers, serialization, SQL, filesystem, subprocess, network, permissions, or private data) requires dedicated human review.
- Use least privilege: workspace-scoped writes, network/secret access only when approved, no autonomous merge/deploy, and exact command/result provenance.
- Measure AI impact with lead time, review time, CI failures, reverts, escaped defects, and churn; do not infer productivity from self-report.

### Semantic source-tree hierarchy

- Do **not** balance source folders like AVL/B-trees. Package boundaries follow information hiding, cohesion, coupling, public contracts, ownership, and change patterns; naturally heavy-tailed sizes are expected.
- Empty marker packages and speculative folder scaffolds are forbidden unless an exact, dated structural-role exception exists. Keep future plans in architecture/roadmap documents.
- `__init__.py` is a compatibility/public facade only: imports, re-exports, `__all__`, metadata, and bounded lazy hooks. Domain classes and business functions belong in cohesive modules.
- Severe branch concentration is a review trigger, not a command to redistribute files. Fix it only when dependency, churn, ownership, or comprehension evidence shows a bad boundary.

- AI/hierarchy policy: `python3 scripts/check_ai_hierarchy_policy.py`
### GitHub Actions supply-chain controls

- Pin every third-party action to a full-length commit SHA; keep the human-readable release in a comment.
- Declare least-privilege workflow `permissions`; read-only `contents` is the default.
- Set `persist-credentials: false` on checkout and provide narrowly scoped credentials only to the step that needs mutation.
- Validate workflow changes with `python scripts/test_ai_hierarchy_policy.py`, `pinact run --fix=false --no-api`, and `uvx zizmor --offline --min-severity medium .github/workflows`.
