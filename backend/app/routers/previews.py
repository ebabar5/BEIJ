from fastapi import APIRouter, status
from typing import List
from app.schemas.product_preview import ProductPreview
from app.services.preview_service import *

router = APIRouter(prefix="/previews", tags=["previews"])

@router.get("",response_model=List[ProductPreview])
def getPreviews():
    return get_all_product_previews()

