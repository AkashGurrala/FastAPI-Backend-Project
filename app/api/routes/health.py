from fastapi  import APIRouter
from datetime import datetime
from app.core.config import ENV

router = APIRouter()

@router.get("/health")
def health_check():
    return{
        "status": "ok",
        "service": "product-api",
        "version": "0.1",
        "environment": ENV,
        "time": datetime.utcnow()
    }
