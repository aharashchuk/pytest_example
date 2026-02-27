"""CSV parsing utility — stdlib ``csv.DictReader`` only, no third-party parser."""

from __future__ import annotations

import csv
import io

CsvRecord = dict[str, str]


def parse_csv_to_records(text: str) -> list[CsvRecord]:
    """Parse a CSV *text* string into a list of row dicts.

    Features:
    - Strips a leading UTF-8 BOM (``\\uFEFF``) if present.
    - Auto-detects delimiter: picks ``;`` when there are more semicolons than
      commas in the header line, otherwise defaults to ``,``.
    - Deduplicates repeated header names by appending ``__2``, ``__3``, etc.
    - Skips fully-empty rows.

    Returns:
        A list of ``dict[str, str]`` — one entry per non-empty data row.
    """
    # Strip BOM
    text = text.lstrip("\ufeff")

    if not text.strip():
        return []

    first_line = text.split("\n", 1)[0]
    delimiter = ";" if first_line.count(";") > first_line.count(",") else ","

    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)

    # Deduplicate headers that DictReader may have already renamed with a None key
    raw_fieldnames: list[str] = list(reader.fieldnames or [])
    seen: dict[str, int] = {}
    clean_fieldnames: list[str] = []
    for name in raw_fieldnames:
        base = (name or "").strip() or f"__col_{len(clean_fieldnames) + 1}"
        count = seen.get(base, 0) + 1
        seen[base] = count
        clean_fieldnames.append(base if count == 1 else f"{base}__{count}")

    records: list[CsvRecord] = []
    for raw_row in reader:
        row = dict(zip(clean_fieldnames, raw_row.values(), strict=False))
        # Skip rows where every value is empty
        if all(v.strip() == "" for v in row.values()):
            continue
        records.append(row)

    return records
