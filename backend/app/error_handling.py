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

# this deals with the AppError subclasses, format {message, code}
def register_errors(app):
    # AppError into JSON shape 
    @app.exception_handler(AppError)
    def handle_app_error(request: Request, exc: AppError):
        return JSONResponse(
            status_code = exc.status_code,
            content = {"message": exc.message, "code": exc.code},
        )
    
    # AppError for http errors
    @app.exception_handler(HTTPException)
    def handle_http_exception(request: Request, exc: HTTPException):
        if exc.status_code == 404:
            e = NotFound()
            return JSONResponse(status_code = e.status_code, content = {"message": e.message, "code": e.code})
        if exc.status_code == 400:
            e = BadRequest()
            return JSONResponse(status_code = e.status_code, content = {"message": e.message, "code": e.code})
        return JSONResponse(
            status_code = exc.status_code,
            content = {"message": exc.detail, "code": f"http_{exc.status_code}"}
        )
        
    # AppError for preventing info getting to users 
    @app.exception_handler(Exception)
    def handle_unexpected(request: Request, exc: Exception):
        e = AppError()
        return JSONResponse(status_code = e.status_code, content = {"message": e.message, "code": e.code})