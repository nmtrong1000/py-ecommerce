from fastapi.encoders import jsonable_encoder
from datetime import datetime, timezone
from app.shared.api_response import ResponseData

"""
Override the default Swagger UI documentation
"""


def custom_swagger_docs(app):
  original_openapi = app.openapi

  def custom_openapi():
    if app.openapi_schema:
      return app.openapi_schema

    # Get the original OpenAPI schema
    openapi_schema = original_openapi()
    example_response = ResponseData(
      success=False,
      message="Invalid data",
      statusCode=422,
      data=None,
      timestamp=datetime.now(timezone.utc),
    )

    # Iterate through all paths and methods
    for _, methods in openapi_schema["paths"].items():
      for _, method in methods.items():
        responses = method.get("responses", {})

        if "422" in responses:
          # Patch only the content/example
          content = responses["422"].get("content", {})
          content["application/json"] = {"example": jsonable_encoder(example_response)}

    app.openapi_schema = openapi_schema
    return app.openapi_schema

  app.openapi = custom_openapi
