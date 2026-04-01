from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel
from datetime import datetime, timezone

T = TypeVar("T")


class ResponseData(BaseModel, Generic[T]):
  success: bool
  message: str
  statusCode: int
  data: Optional[T] = None
  timestamp: datetime = datetime.now(timezone.utc)


# Response normalizer
class ApiResponse:
  @staticmethod
  def ok(
    data: T, status_code: int = status.HTTP_200_OK, message: str = "Success"
  ) -> Response:
    response_data = ResponseData(
      success=True,
      message=message,
      statusCode=status_code,
      data=data,
    )
    return JSONResponse(
      status_code=status_code,
      content=jsonable_encoder(response_data),
    )

  @staticmethod
  def fail(status_code: int, message: str = "Not found") -> Response:
    response_data = ResponseData(
      success=False,
      message=message,
      statusCode=status_code,
    )
    return JSONResponse(
      status_code=status_code,
      content=jsonable_encoder(response_data),
    )

  @staticmethod
  def not_found(message: str = "Not found") -> Response:
    return ApiResponse.fail(status_code=status.HTTP_404_NOT_FOUND, message=message)

  @staticmethod
  def invalid_data(message: str = "Invalid data") -> Response:
    return ApiResponse.fail(
      status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, message=message
    )
