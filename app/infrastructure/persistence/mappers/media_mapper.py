from dataclasses import asdict
import json
from typing import Optional
from app.domain.entities.media_entity import Media, MediaListResult
from app.infrastructure.persistence.models.media_model import MediaModel


class MediaMapper:
  @staticmethod
  def to_entity(model: MediaModel) -> Optional[Media]:
    if not model:
      return None

    return Media(
      id=model.id,
      url=str(model.url),
      media_type=model.media_type,
      mime_type=model.mime_type,
      size=model.size,
      created_at=model.created_at,
      updated_at=model.updated_at,
    )

  @staticmethod
  def to_model(entity: Media) -> Optional[MediaModel]:
    if not entity:
      return None

    return MediaModel(
      id=entity.id,
      url=str(entity.url),
      media_type=entity.media_type,
      mime_type=entity.mime_type,
      size=entity.size,
    )

  @staticmethod
  def from_json(json_str: str) -> Optional[Media]:
    data = json.loads(json_str)
    if not data:
      return None

    return Media(**data)

  @staticmethod
  def to_json(entity: Media) -> str:
    return json.dumps(
      {
        **asdict(entity),
        "id": str(entity.id),
        "created_at": entity.created_at.isoformat(),
        "updated_at": entity.updated_at.isoformat(),
      }
    )

  @staticmethod
  def from_list_json(json_str: str) -> MediaListResult:
    data = json.loads(json_str)
    if not data:
      return None

    data["items"] = [Media(**json.loads(item)) for item in data["items"]]
    return MediaListResult(**data)

  @staticmethod
  def to_list_json(data: MediaListResult) -> str:
    return json.dumps(
      {**asdict(data), "items": [MediaMapper.to_json(item) for item in data.items]}
    )

  @staticmethod
  def update_model(model: MediaModel, entity: Media) -> None:
    model.url = entity.url
    model.media_type = entity.media_type
    model.mime_type = entity.mime_type
    model.size = entity.size

    return model
