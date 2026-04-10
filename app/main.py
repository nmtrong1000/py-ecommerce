from fastapi import FastAPI
from app.shared.exception_handlers import register_exception_handlers
from app.shared.custom_openapi import custom_swagger_docs
from app.presentation.controllers.media_controller import router as media_router


app = FastAPI()

register_exception_handlers(app)
custom_swagger_docs(app)

app.include_router(media_router, prefix="/media")
