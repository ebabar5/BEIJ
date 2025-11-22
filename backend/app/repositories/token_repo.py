from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from app.repositories.repository_helpers import load_json_data, save_json_data

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "tokens.json"

def load_all() -> List[Dict[str, Any]]:
    return load_json_data(DATA_PATH)

def save_all(tokens: List[Dict[str, Any]]) -> None:
    save_json_data(DATA_PATH, tokens)

def add_token(token: Dict[str, Any]) -> None:
    tokens = load_all()
    tokens.append(token)
    save_all(tokens)

def remove_token(token: str) -> None:
    tokens = load_all()
    save_all([t for t in tokens if t.get("token") != token])

def get_token(token: str) -> Dict[str, Any] | None:
    tokens = load_all()
    return next((t for t in tokens if t.get("token") == token), None)

def remove_expired_tokens() -> None:
    tokens = load_all()
    now_iso = datetime.now().isoformat()
    save_all([t for t in tokens if t.get("expires_at", "") > now_iso])

def remove_user_tokens(user_id: str) -> None:
    tokens = load_all()
    save_all([t for t in tokens if t.get("user_id") != user_id])
