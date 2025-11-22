from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

# small app errors 
class AppError(Exception):
    status_code = 500
    code = "internal_error" 
    message = "Something went wrong."
    def __init__(self, message=None):
        if message is not None:
            self.message = message

# when a product doesn't exist
class NotFound(AppError):
    status_code = 404
    code = "not_found" 
    message = "We could not find what you were looking for."

# when client has sent a bad or invalid request 
class BadRequest(AppError):
    status_code = 400
    code = "bad_request"
    message = "Your request had a problem, please try again."

# New helpers (refactoring) 
def _to_json(e: AppError) -> JSONResponse:
    return JSONResponse(
        status_code = e.status_code,
        content = {"message": e.message, "code": e.code}, 
    )
# New map for HTTP status codes to our custom errors
HTTP_ERROR_MAP = {
    404: NotFound, 
    400: BadRequest,
}

# this deals with the AppError subclasses, format {message, code}
def register_errors(app):
    # AppError into JSON shape 
    @app.exception_handler(AppError)
    def handle_app_error(request: Request, exc: AppError):
        return _to_json(exc)
    
    # AppError for http errors
    @app.exception_handler(HTTPException)
    def handle_http_exception(request: Request, exc: HTTPException):
        mapped_error = HTTP_ERROR_MAP.get(exc.status_code)
        # if it's a mapped status code (404/400), return custom format  
        if mapped_error is not None:
            return _to_json(mapped_error())

        # otherwise return FastAPI's detail, still in our custom format 
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail, "code": f"http_{exc.status_code}"},
        )
        
    # AppError for preventing info getting to users/catches any unexpected errors 
    @app.exception_handler(Exception)
    def handle_unexpected(request: Request, exc: Exception):
        return _to_json(AppError())