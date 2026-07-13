# MailReader

Placeholder repository for the intended goal: reading email data into CSV.

## Current status

This repository does not currently contain an implementation. The committed
contents are only:

- `README.md`
- `LICENSE` (MIT)

There are no source files, requirements, examples, tests, fixtures, or documented
setup commands in this checkout. Because of that, there is no honest install or
test workflow to run yet.

## Intended direction

A future implementation could add:

1. an email input contract, such as exported mailbox files or an IMAP adapter
   with credentials kept out of git;
2. a CSV schema for selected message fields;
3. a parser with deterministic fixtures;
4. tests that verify parsing, privacy handling, and CSV output.

Until those pieces are committed, treat this repo as a legacy placeholder rather
than a working mail-to-CSV tool.
