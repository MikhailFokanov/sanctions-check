from loguru import logger
from fastapi import APIRouter, Depends
from src.database import get_db
from src.database.db import Database
from src.search.people_search import PeopleSearch
from src.search import get_search_obj


main_router = APIRouter(
   prefix='',
   tags=['search']
)


@main_router.get("/search")
async def search_person(pattern, ps: PeopleSearch = Depends(get_search_obj)):        
    res = ps.search(pattern)
    logger.info(res)
    return {"message": res} 


@main_router.get("/history")
async def get_previous_search_results():
    return {"message": "/results request"} 