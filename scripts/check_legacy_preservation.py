#!/usr/bin/env python3
"""Verify immutable archived bytes and syntax without importing legacy source."""

from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = Path("legacy/2022-mailreader")
SOURCE_COMMIT = "3658fddcd5e796b9bcb2b8a9231aa3db64bfd2ec"
SOURCE_INVENTORY_SHA256 = "179144f6531c3d9072c0fa7771df002ea62d14e82d9889d3ca885ba781645e02"


def validate(root: Path) -> list[str]:
    archive = root / ARCHIVE
    errors: list[str] = []
    try:
        manifest = json.loads((archive / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"archive manifest unreadable: {exc}"]
    if not isinstance(manifest, dict):
        return ["archive manifest must be an object"]
    if manifest.get("schema_version") != 1 or manifest.get("source_commit") != SOURCE_COMMIT:
        errors.append("archive identity differs from reviewed original history")
    records = manifest.get("files", [])
    if not isinstance(records, list) or len(records) != 27:
        return [*errors, "archive manifest must contain all 27 original blobs"]
    if not all(isinstance(record, dict) for record in records):
        return [*errors, "archive manifest file records must be objects"]
    inventory = json.dumps(
        sorted(records, key=lambda item: str(item.get("original_path", ""))),
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    if hashlib.sha256(inventory).hexdigest() != SOURCE_INVENTORY_SHA256:
        errors.append("archive inventory differs from reviewed original baseline")
    expected = {"manifest.json", "README.md"}
    for record in records:
        if not isinstance(record, dict):
            errors.append("archive manifest file record must be an object")
            continue
        original = Path(str(record.get("original_path", "")))
        mapped = ARCHIVE / original
        if original.is_absolute() or ".." in original.parts or not original.parts:
            errors.append("archive manifest contains unsafe original path")
            continue
        if record.get("archived_path") != mapped.as_posix():
            errors.append(f"archive mapping mismatch: {original}")
        if original.as_posix() in expected:
            errors.append(f"duplicate or reserved archive path: {original}")
        expected.add(original.as_posix())
        path = root / mapped
        if path.is_symlink() or not path.is_file():
            errors.append(f"archived file missing or symlinked: {original}")
            continue
        data = path.read_bytes()
        git_blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if len(data) != record.get("bytes") or hashlib.sha256(data).hexdigest() != record.get("sha256") or git_blob != record.get("git_blob_sha"):
            errors.append(f"archived bytes changed: {original}")
        if path.suffix == ".py":
            try:
                ast.parse(data.decode("utf-8"), filename=mapped.as_posix())
            except (SyntaxError, UnicodeError) as exc:
                errors.append(f"archived syntax invalid: {original}: {exc}")
    actual = {p.relative_to(archive).as_posix() for p in archive.rglob("*") if p.is_file() or p.is_symlink()}
    if actual != expected:
        errors.append(f"archive inventory changed: missing={sorted(expected - actual)}, extra={sorted(actual - expected)}")
    return errors


def main() -> int:
    errors = validate(ROOT)
    if errors:
        print("\n".join(errors))
        return 1
    print("legacy preservation OK: 27 original blobs; syntax checked; source not imported")
    return 0


if __name__ == "__main__":
    sys.exit(main())

