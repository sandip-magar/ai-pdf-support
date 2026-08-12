from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
import logging

#set up 
logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s -%(levelname)s -%(message)s"
)

#This function will handle the HTTPException error(200, 300, 400)
async def HTTPException_handler(request: Request, exc: HTTPException):
    logging.error(f" HTTPException error on {request.url.path} : {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            }
        },
    )

#This function wull handle the validation error(when user send the bad json)
async def validation_errorh_handler(request: Request, exc: RequestValidationError):
    logging.error(f" Validation error on {request.url.path} : {exc.errors}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "success": False,
            "error": {
                "code": 422,
                "message": "Validation Failed",
                "details": jsonable_encoder(exc.errors()) #this will show where is the main error
            }
        },
    )

#This function will handle the server crash error(500 internal server error)
async def unexpected_error_handler(request: Request, exc: Exception):
    logging.error(f" Unexpected error on {request.url.path} : {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error":{
                "code": 500,
                "details": "Internal Server Error Occured"
            }
        },
    )