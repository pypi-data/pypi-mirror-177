"""Model utilities."""
from __future__ import annotations

from pathlib import Path
from typing import Union

SUFFIXES: tuple[str, ...] = (".json.gz", ".json", ".jpg", ".jpeg", ".png")


def get_slug(path: Union[str, Path], suffixes: tuple[str, ...] = SUFFIXES) -> str:
    """Get the slug (filename without extension suffix) for a path."""
    path = Path(path)
    filename = path.name
    for suffix in suffixes:
        if filename.endswith(suffix):
            filename = filename[: -len(suffix)]
    return filename
