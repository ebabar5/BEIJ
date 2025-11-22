from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from app.error_handling import AppError, NotFound, BadRequest, register_errors

# create a mock test app to test error handling classes 
def create_test_app() -> FastAPI:
    app = FastAPI()
    register_errors(app)

    @app.get("/app-error")
    def raise_app_error():
        raise AppError("App error")

    @app.get("/not-found")
    def raise_not_found_error():
        raise NotFound()

    @app.get("/http-400")
    def raise_http_400():
        raise HTTPException(status_code = 400, detail = "error here")

    @app.get("/http-404")
    def raise_http_404():
        raise HTTPException(status_code = 404, detail = "other error here")

    return app

# test the app error handler, matching the format of the error_handling file
def test_app_error_handler():
    app = create_test_app()
    client = TestClient(app)
    
    r = client.get("/app-error")
    assert r.status_code == 500
    assert r.json() == {
        "message": "App error",
        "code": "internal_error",
    }
def test_not_found_app_error():
    app = create_test_app()
    client = TestClient(app)

    r = client.get("/not-found")
    assert r.status_code == 404
    assert r.json() == {
        "message": "We could not find what you were looking for.",
        "code": "not_found",
    }
def test_bad_request():
    app = create_test_app()
    client = TestClient(app)

    r = client.get("/http-400")
    assert r.status_code == 400
    assert r.json() == {
        "message": "Your request had a problem, please try again.",
        "code": "bad_request",
    }


