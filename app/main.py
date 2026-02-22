from fastapi import FastAPI, Request
from app.api.routes import products, health
from app.core.logger import logger
import time
from fastapi.responses import JSONResponse
from app.services.product_service import InvalidInputException, NoProductFoundException
import traceback
import uuid


app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id=str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    logger.info(f"[{request_id}] Incoming Request: {request.method} {request.url}")

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"[{request_id}] Completed {request.method} {request.url} with status {response.status_code} in {process_time:.4f}s")

    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception at {request.method} {request.url} | Error: {str(exc)}")
    
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content= {"detail": "Internal Server Crash"}
        )

@app.exception_handler(InvalidInputException)
async def invalid_input_exception_handler(request: Request, exc: InvalidInputException):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )

@app.exception_handler(NoProductFoundException)
async def product_not_found_exception(request: Request, exc: NoProductFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

app.include_router(products.router)
app.include_router(health.router)

logger.info("App started")

@app.get("/")
def greet():
    return "Hey there!"