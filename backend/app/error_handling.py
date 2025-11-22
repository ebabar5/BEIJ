from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

class AppError(Exception):
    status_code = 500
    code = "internal_error" 
    message = "Something went wrong."
    def __init__(self, message=None):
        if message is not None:
            self.message = message

class NotFound(AppError):
    status_code = 404
    code = "not_found" 
    message = "We could not find what you were looking for."

class BadRequest(AppError):
    status_code = 400
    code = "bad_request"
    message = "Your request had a problem, please try again."

def _to_json(e: AppError) -> JSONResponse:
    return JSONResponse(
        status_code = e.status_code,
        content = {"message": e.message, "code": e.code}, 
    )

HTTP_ERROR_MAP = {
    404: NotFound, 
    400: BadRequest,
}

def register_errors(app):
    @app.exception_handler(AppError)
    def handle_app_error(request: Request, exc: AppError):
        return _to_json(exc)
    
    @app.exception_handler(HTTPException)
    def handle_http_exception(request: Request, exc: HTTPException):
        mapped_error = HTTP_ERROR_MAP.get(exc.status_code)
        if mapped_error is not None:
            return _to_json(mapped_error())

        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail, "code": f"http_{exc.status_code}"},
        )
        
    @app.exception_handler(Exception)
    def handle_unexpected(request: Request, exc: Exception):
        return _to_json(AppError())