from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHttpException
from app.shared.api_response import ApiResponse


async def http_exception_handler(_: Request, e: HTTPException):
  return ApiResponse.fail(status_code=e.status_code, message=e.detail)


async def validation_exception_handler(_: Request, e: RequestValidationError):
  return ApiResponse.invalid_data(message=str(e.errors()))


async def value_exception_handler(_: Request, e: ValueError):
  return ApiResponse.invalid_data(message=str(e))


async def starlette_exception_handler(_: Request, e: StarletteHttpException):
  if e.status_code == status.HTTP_404_NOT_FOUND:
    return ApiResponse.not_found(message="API not found")

  return ApiResponse.fail(status_code=e.status_code, message=e.detail)


async def system_exception_handler(_: Request, e: Exception):
  return ApiResponse.fail(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(e)
  )


def register_exception_handlers(app: FastAPI):
  app.add_exception_handler(HTTPException, http_exception_handler)
  app.add_exception_handler(RequestValidationError, validation_exception_handler)
  app.add_exception_handler(ValueError, value_exception_handler)
  app.add_exception_handler(StarletteHttpException, starlette_exception_handler)
  app.add_exception_handler(Exception, system_exception_handler)
