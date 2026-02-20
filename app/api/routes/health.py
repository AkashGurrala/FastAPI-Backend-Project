import os
from fastapi  import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/health")
def health_check():
    return{
        "status": "ok",
        "service": "product-api",
        "version": "0.1",
        "environment": os.getenv("ENV", "dev"),
        "time": datetime.utcnow()
    }