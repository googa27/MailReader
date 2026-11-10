# Archived 2022 MailReader prototype

This directory preserves all 27 blobs from `googa27/MailReader` branch `master`, commit `3658fddcd5e796b9bcb2b8a9231aa3db64bfd2ec` (2022-05-15). Original paths are prefixed by `legacy/2022-mailreader/`; source bytes, original names and attribution are unchanged. [manifest.json](manifest.json) records original paths, Git blob identities, SHA-256 and byte counts.

The 14 original commits form a separate history from the governance default branch. Integration must retain that tip as a parent ancestor. This notice and the manifest are new preservation metadata, not original implementation files.

**Do not use the demo with real mail.** The archive has no supported runtime or dependency lock. No archived module is imported by preservation checks or a supported application. Its internal `src.*` imports remain historical and are not exposed as a root package.

| Inherited defect | Required revival work |
|---|---|
| Gmail list reads only one page and assumes messages exist | Test pagination, empty results and typed failures with a synthetic Google client |
| Timestamp/date dictionaries overwrite purchases | Preserve message identity and aggregate every order, including same-day purchases |
| First settlement calls `max()` without initial data; save date is fixed at import | Define initial cutoff, call-time date and output directory policy |
| Fixed MIME-part/cell positions and custom date format | Use maintained MIME/HTML parsing behind bounded receipt adapters |
| Token JSON is written beneath source; parsed content is printed | Secure credential storage, redaction and retention rules before any live use |

The historical ignore file does not cover the actual credential data directory. Root ignore rules now cover archived credential and output paths; they do not make historical authentication safe.

No private mailbox, credential, token or settlement data was added. A bounded review of all 37 unique blobs across the 14 commits found no credential-format, email-literal or absolute-user-path matches; that is not a general security certification.

Root [LICENSE](../../LICENSE) remains MIT. Original linked commit author: `googa27`. For future work use the maintained providers documented in [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md), after the revival gates pass.

