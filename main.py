from fastapi import FastAPI, HTTPException
from routers.auth import router as auth_router
from core.extension import HTTPException_handler, unexpected_error_handler, validation_errorh_handler
from fastapi.exceptions import RequestValidationError
from routers.users import router as user_router
from ai.file_upload import router as ai_router
from chat.history import router as history_router
from ai.ask_question import router as ask_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/api/user", tags=["Users"])
app.include_router(ai_router, prefix="/api/ai", tags=["PDF File handle"])
app.include_router(history_router, prefix="/api/history", tags=["History Cleaner"])
app.include_router(ask_router, prefix="/api/ai", tags=["ASK-AI"])
app.add_exception_handler(HTTPException, HTTPException_handler)
app.add_exception_handler(RequestValidationError, validation_errorh_handler)
app.add_exception_handler(Exception, unexpected_error_handler)


@app.get("/")
def home():
    return {"messages": "Welcome to AI PDF Support API"}