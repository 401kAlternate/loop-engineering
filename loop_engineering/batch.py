"""Run a fixed-width transaction batch and optionally compare it with a golden file."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

RECORD_WIDTH = 20
ACCOUNT_WIDTH = 10
AMOUNT_WIDTH = 10


@dataclass(frozen=True)
class Transaction:
    account: str
    amount_cents: int


def parse_line(line: str, line_number: int) -> Transaction:
    value = line.rstrip("\n\r")
    if not value:
        raise ValueError(f"line {line_number}: blank records are not allowed")
    if len(value) != RECORD_WIDTH:
        raise ValueError(
            f"line {line_number}: expected {RECORD_WIDTH} characters, got {len(value)}"
        )
    account = value[:ACCOUNT_WIDTH].strip()
    raw_amount = value[ACCOUNT_WIDTH:]
    if not account:
        raise ValueError(f"line {line_number}: account is required")
    try:
        amount = Decimal(raw_amount) / Decimal(100)
    except InvalidOperation as exc:
        raise ValueError(f"line {line_number}: invalid amount {raw_amount!r}") from exc
    return Transaction(account, int(amount * 100))


def summarize(input_path: Path) -> str:
    transactions = [
        parse_line(line, number)
        for number, line in enumerate(input_path.read_text().splitlines(), start=1)
    ]
    total = sum(item.amount_cents for item in transactions)
    return f"TRANSACTION-COUNT {len(transactions):010d}\nTOTAL-CENTS      {total:010d}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--golden", type=Path)
    args = parser.parse_args()
    result = summarize(args.input)
    args.output.write_text(result)
    if args.golden:
        expected = args.golden.read_text()
        if result != expected:
            print("FAIL: generated output differs from golden output")
            return 1
        print("PASS: generated output matches golden output")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
