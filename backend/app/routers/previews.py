from fastapi import APIRouter
from typing import List
from app.schemas.product_preview import ProductPreview
from app.services.preview_service import *

router = APIRouter(prefix="/previews", tags=["previews"])

@router.get("",response_model=List[ProductPreview])
def getPreviews():
    return get_all_product_previews()

@router.get("/{fil}",response_model=List[ProductPreview])
def filterPreviews(fil:str=""):
    return filter_previews(fil)


#'''Putting this here as for some reason a seperate searchs.py file isn't working
from app.services.search_service import *

@router.get("/search/",response_model=str)
def no_search_entry():
    return "Please enter a search query"

#wide search
@router.get("/search/w={search_string}",response_model=List[ProductPreview])
def keywordSearch(search_string:str):
    keywords = search_string.split(" ")
    return parse_to_previews(keyword_search(keywords))

#strict search[default]
@router.get("/search/{search_string}",response_model=List[ProductPreview])
def keywordSearch(search_string:str):
    keywords = search_string.split(" ")
    return parse_to_previews(keyword_search(keywords,strict=True))
#'''