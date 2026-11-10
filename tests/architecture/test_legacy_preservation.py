"""Source preservation gates must detect drift without importing old runtime."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("legacy_preservation_gate", ROOT / "scripts/check_legacy_preservation.py")
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def test_original_archive_matches_reviewed_manifest() -> None:
    assert gate.validate(ROOT) == []


def test_archive_gate_rejects_source_drift(tmp_path: Path) -> None:
    shutil.copytree(ROOT / gate.ARCHIVE, tmp_path / gate.ARCHIVE)
    source = tmp_path / gate.ARCHIVE / "src/CONFIG.py"
    source.write_text(source.read_text() + "\n# changed\n")
    assert any("archived bytes changed" in error for error in gate.validate(tmp_path))


def test_archive_gate_rejects_new_private_output_path(tmp_path: Path) -> None:
    shutil.copytree(ROOT / gate.ARCHIVE, tmp_path / gate.ARCHIVE)
    output = tmp_path / gate.ARCHIVE / "Outputs/settlements/synthetic.xlsx"
    output.parent.mkdir(parents=True)
    output.write_bytes(b"synthetic placeholder; not a workbook")
    assert any("archive inventory changed" in error for error in gate.validate(tmp_path))


def test_archive_gate_rejects_coordinated_source_and_manifest_changes(tmp_path: Path) -> None:
    shutil.copytree(ROOT / gate.ARCHIVE, tmp_path / gate.ARCHIVE)
    archive = tmp_path / gate.ARCHIVE
    source = archive / "src/CONFIG.py"
    data = source.read_bytes() + b"\n# coordinated change\n"
    source.write_bytes(data)
    path = archive / "manifest.json"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    record = next(item for item in manifest["files"] if item["original_path"] == "src/CONFIG.py")
    record["bytes"] = len(data)
    record["sha256"] = hashlib.sha256(data).hexdigest()
    record["git_blob_sha"] = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
    path.write_text(json.dumps(manifest), encoding="utf-8")
    assert any("reviewed original baseline" in error for error in gate.validate(tmp_path))

