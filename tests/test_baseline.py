from pathlib import Path

from loop_engineering.batch import summarize


ROOT = Path(__file__).resolve().parents[1]


def test_baseline_matches_golden_output():
    input_path = ROOT / "examples/baseline/transactions.dat"
    expected_path = ROOT / "examples/baseline/expected-summary.out"
    assert summarize(input_path) == expected_path.read_text()


def test_baseline_artifacts_exist():
    baseline_dir = ROOT / "examples/baseline"
    assert (baseline_dir / "transactions.dat").exists()
    assert (baseline_dir / "expected-summary.out").exists()
    assert (baseline_dir / "job-log.txt").exists()
    assert (baseline_dir / "transaction-trace.txt").exists()
