# src/logic/repo.py
from typing import Optional, List
from models.io_models import SessionConfigDTO
from logic.db import get_db

COLL = "vibe_configs"

def _coll():
    return get_db().collection(COLL)

def save_config(cfg: SessionConfigDTO) -> str:
    _coll().document(cfg.id).set(cfg.model_dump())
    return cfg.id

def load_config(cfg_id: str) -> Optional[SessionConfigDTO]:
    doc = _coll().document(cfg_id).get()
    return SessionConfigDTO(**doc.to_dict()) if doc.exists else None

def list_configs(limit: int = 50) -> List[SessionConfigDTO]:
    q = _coll().order_by("name").limit(limit).stream()
    return [SessionConfigDTO(**d.to_dict()) for d in q]

def search_configs(prefix: str, limit: int = 50) -> List[SessionConfigDTO]:
    if not prefix:
        return list_configs(limit)
    end = prefix + u"\uf8ff"  # prefix range end
    q = (_coll()
         .where("name", ">=", prefix)
         .where("name", "<=", end)
         .order_by("name")
         .limit(limit)
         .stream())
    return [SessionConfigDTO(**d.to_dict()) for d in q]

def delete_config(cfg_id: str) -> None:
    _coll().document(cfg_id).delete()
