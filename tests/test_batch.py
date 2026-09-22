from pathlib import Path

from loop_engineering.batch import summarize


ROOT = Path(__file__).parents[1]
INPUT = ROOT / "examples/transactions/input.dat"
EXPECTED = ROOT / "examples/transactions/expected.out"


def test_transaction_summary_matches_golden_file():
    assert summarize(INPUT) == EXPECTED.read_text()


def test_malformed_record_is_rejected(tmp_path):
    bad = tmp_path / "bad.dat"
    bad.write_text("too short\n")
    try:
        summarize(bad)
    except ValueError as error:
        assert "expected 20 characters" in str(error)
    else:
        raise AssertionError("malformed records must fail validation")
