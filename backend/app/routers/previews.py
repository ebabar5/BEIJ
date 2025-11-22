from fastapi import APIRouter
from typing import List
from app.schemas.product_preview import ProductPreview
from app.services.preview_service import (
    get_all_product_previews,
    filter_previews,
    parse_to_previews,
)

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

# shared logic for both wide and strict search[default] endpoints, accepts optional filter after '&'
def _keyword_search_impl(search_string: str):
    splice = search_string.split("&", 1)
    keywords = splice[0].split(" ")
    if len(splice) > 1:
        return parse_to_previews(keyword_search(keywords, filter = splice[1]))
    return parse_to_previews(keyword_search(keywords))

# wide search
@router.get("/search/w={search_string}", response_model=List[ProductPreview])
def keyword_search_wide(search_string: str):
    return _keyword_search_impl(search_string)


# strict search [default]
@router.get("/search/{search_string}", response_model=List[ProductPreview])
def keyword_search_strict(search_string: str):
    return _keyword_search_impl(search_string)