from pathlib import Path
from typing import List, Dict, Any
from app.repositories.repository_helpers import load_json_data, save_json_data

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "products.json"

def load_all() -> List[Dict[str, Any]]:
    return load_json_data(DATA_PATH)

def save_all(items: List[Dict[str, Any]]) -> None:
    save_json_data(DATA_PATH, items)
