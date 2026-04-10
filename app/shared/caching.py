from typing import Dict, Any
import json


def _serialize_filters(filters: Dict[str, Any]) -> str:
  if filters is None:
    return "none"

  return json.dumps(filters, sort_keys=True, separators=(",", ":"))


def build_get_key(entity_id: str, item_id: str) -> str:
  return f"{entity_id}:get:{item_id}"


def build_list_key(
  entity_id: str,
  page: int,
  page_size: int,
  filters: dict,
  sort_by: str,
  sort_order: str,
) -> str:
  return (
    f"{entity_id}:list:"
    f"page:{page}"
    f"page_size:{page_size}"
    f"filters:{_serialize_filters(filters)}"
    f"sort_by:{sort_by}"
    f"sort_order:{sort_order}"
  )
