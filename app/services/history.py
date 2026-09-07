# Copyright (c) 2026 TW4RDYDEV. All rights reserved.

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse

from PySide6.QtCore import QStandardPaths


MAX_HISTORY = 50


def _app_data_dir() -> Path:
    base = Path(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
    base.mkdir(parents=True, exist_ok=True)
    return base


def _url_to_path(value: str) -> Path:
    if value.startswith("file:"):
        parsed = urlparse(value)
        path = unquote(parsed.path)
        if parsed.netloc:
            path = f"//{parsed.netloc}{path}"

        # Windows file URLs look like /C:/path
        if len(path) >= 3 and path[0] == "/" and path[2] == ":":
            path = path[1:]

        return Path(path)

    return Path(value)


class HistoryService:
    def __init__(self, load_persisted: bool = True) -> None:
        self.path = _app_data_dir() / "history.json"
        self._items: list[dict] = []

        if load_persisted:
            self.load()

    @property
    def items(self) -> list[dict]:
        return list(self._items)

    def load(self) -> None:
        if not self.path.exists():
            self._items = []
            return

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self._items = data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError):
            self._items = []

    def save(self) -> None:
        self.path.write_text(
            json.dumps(self._items, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def remove_persisted(self) -> None:
        try:
            self.path.unlink(missing_ok=True)
        except OSError:
            pass

    def add(self, item: dict, remember: bool) -> None:
        self._items.insert(0, item)
        self._items = self._items[:MAX_HISTORY]
        if remember:
            self.save()

    def delete(self, index: int, remember: bool) -> None:
        if 0 <= index < len(self._items):
            self._items.pop(index)
            if remember:
                self.save()

    def clear(self, remember: bool) -> None:
        self._items.clear()
        if remember:
            self.save()

    def export(self, destination: str, file_type: str) -> Path:
        path = _url_to_path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)

        if file_type.lower() == "csv":
            if path.suffix.lower() != ".csv":
                path = path.with_suffix(".csv")
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle)
                writer.writerow(
                    ["Timestamp", "Input", "Input Base", "Decimal", "Binary", "Octal", "Hexadecimal"]
                )
                for item in self._items:
                    writer.writerow(
                        [
                            item.get("timestamp", ""),
                            item.get("input", ""),
                            item.get("inputBase", ""),
                            item.get("decimal", ""),
                            item.get("binary", ""),
                            item.get("octal", ""),
                            item.get("hexadecimal", ""),
                        ]
                    )
        else:
            if path.suffix.lower() != ".txt":
                path = path.with_suffix(".txt")
            lines = [
                "Number System Converter v1.0.0 — Conversion History",
                "=" * 58,
                "",
            ]
            for item in self._items:
                lines.append(
                    f"[{item.get('timestamp', '')}] "
                    f"{item.get('input', '')} ({item.get('inputBase', '')}) "
                    f"→ DEC {item.get('decimal', '')} | "
                    f"BIN {item.get('binary', '')} | "
                    f"OCT {item.get('octal', '')} | "
                    f"HEX {item.get('hexadecimal', '')}"
                )
            path.write_text("\n".join(lines), encoding="utf-8")

        return path


def build_history_item(input_text: str, result: dict) -> dict:
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "input": input_text,
        "inputBase": result["detectedBase"],
        "decimal": result["decimal"],
        "binary": result["binary"],
        "octal": result["octal"],
        "hexadecimal": result["hexadecimal"],
        "summary": (
            f"{input_text} · {result['detectedBase']} → "
            f"DEC {result['decimal']} · HEX {result['hexadecimal']}"
        ),
    }
