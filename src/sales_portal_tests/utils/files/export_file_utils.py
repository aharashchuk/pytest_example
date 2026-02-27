"""Export file utilities — save Playwright downloads and parse CSV/JSON exports."""

from __future__ import annotations

import json
import os
from pathlib import Path

from playwright.sync_api import Download

from sales_portal_tests.utils.files.csv_utils import parse_csv_to_records

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

ExportedCsvFile = dict[str, object]  # {"format": "csv", "file_path": str, "data": list[CsvRecord]}
ExportedJsonFile = dict[str, object]  # {"format": "json", "file_path": str, "data": object}
ExportedFile = ExportedCsvFile | ExportedJsonFile


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def save_download(download: Download, tmp_path: Path) -> str:
    """Save *download* under *tmp_path* using the suggested filename.

    Args:
        download:  Playwright ``Download`` object.
        tmp_path:  Temporary directory path (e.g. pytest's ``tmp_path`` fixture).

    Returns:
        Absolute path to the saved file as a ``str``.
    """
    suggested = download.suggested_filename
    out_path = tmp_path / suggested
    download.save_as(str(out_path))
    return str(out_path)


def parse_downloaded_export(download: Download, tmp_path: Path) -> ExportedFile:
    """Save *download* and parse it as CSV or JSON based on file extension.

    Args:
        download:  Playwright ``Download`` object.
        tmp_path:  Temporary directory for the saved file.

    Returns:
        A dict with keys ``format``, ``file_path``, and ``data``.
        - ``format``: ``"csv"`` or ``"json"``
        - ``file_path``: absolute path to the saved file
        - ``data``: ``list[CsvRecord]`` for CSV, or parsed Python object for JSON
    """
    file_path = save_download(download, tmp_path)
    ext = os.path.splitext(file_path)[1].lower()
    text = Path(file_path).read_text(encoding="utf-8")

    if ext == ".json":
        return {"format": "json", "file_path": file_path, "data": json.loads(text)}

    # Default/fallback: treat as CSV
    return {"format": "csv", "file_path": file_path, "data": parse_csv_to_records(text)}
