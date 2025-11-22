from pathlib import Path
from typing import List, Dict, Any
from app.error_handling import AppError
from datetime import datetime
from app.repositories.repository_helpers import load_json_data, save_json_data

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "tokens.json"

def load_all() -> List[Dict[str,Any]]:
    return load_json_data(DATA_PATH)

def save_all(tokens: List[Dict[str,Any]]) -> None:
    save_json_data(DATA_PATH, tokens)
    
def add_token(token: Dict [str,Any]) -> None:
    tokens =load_all()
    tokens.append(token)
    save_all(tokens)

def remove_token(token: str) -> None:
    tokens=load_all()
    new_tokens=[it for it in tokens if it.get("token") !=token]
    save_all(new_tokens)

def get_token(token:str) -> Dict[str,Any] | None:
    tokens=load_all()
    for it in tokens:
        if it.get("token") ==token:
            return it
    return None

def remove_expired_tokens() ->None:
    tokens=load_all()
    new_tokens=[it for it in tokens if it.get("expires_at", "") > datetime.now().isoformat()]
    save_all(new_tokens)

def remove_user_tokens(user_id:str) -> None:
    tokens=load_all()
    new_tokens=[it for it in tokens if it.get("user_id") !=user_id]
    save_all(new_tokens)



    

    