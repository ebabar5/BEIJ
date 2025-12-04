from pathlib import Path
import json
import os
import uuid
from typing import List, Dict, Any


def load_json_data(data_path: Path) -> List[Dict[str, Any]]:
    if not data_path.exists():
        return []
    with data_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json_data(data_path: Path, items: List[Dict[str, Any]]) -> None:
    data_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = data_path.with_suffix(f".{uuid.uuid4().hex}.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    os.replace(tmp, data_path)

