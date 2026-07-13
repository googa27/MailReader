from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "scripts" / "check_portfolio_architecture.py"


def test_portfolio_architecture_contract() -> None:
    result = subprocess.run(
        [sys.executable, str(CHECKER)],
        check=False,
        text=True,
        capture_output=True,
        cwd=Path(__file__).resolve().parent,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_architecture_checker_reports_malformed_contract_cleanly(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    spec = importlib.util.spec_from_file_location(
        "mailreader_check_portfolio_architecture",
        CHECKER,
    )
    assert spec is not None and spec.loader is not None
    checker = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checker)

    contract = tmp_path / "docs" / "ARCHITECTURE.yaml"
    contract.parent.mkdir()
    contract.write_text("{not-json\n", encoding="utf-8")
    monkeypatch.setattr(checker, "ROOT", tmp_path)
    monkeypatch.setattr(checker, "CONTRACT", contract)

    exit_code = checker.main()
    captured = capsys.readouterr()
    output = captured.out + captured.err

    assert exit_code == 1
    assert "portfolio architecture check failed:" in captured.out
    assert "docs/ARCHITECTURE.yaml must remain JSON-compatible YAML 1.2" in captured.out
    assert captured.err == ""
    assert "Traceback" not in output
