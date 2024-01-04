from loguru import logger
from fastapi import APIRouter, Depends
from sqlalchemy import select, or_
from src.database import get_db
from src.database.db import Database
from src.database.models import SearchLog
from src.search.people_search import PeopleSearch
from src.search import get_search_obj


main_router = APIRouter(
   prefix='',
   tags=['search']
)


@main_router.get("/search")
async def search_person(name="", address="", ps: PeopleSearch = Depends(get_search_obj)):        
    res = ps.search(name, address)
    logger.info(res)
    return {"message": res} 


@main_router.get("/history")
async def get_previous_search_results(name_pattern="", address_pattern="", return_result=False, db: Database = Depends(get_db)):
    '''This function returns all search requests logged at search_log db table. '''
    requested_fields = [
        SearchLog.id,
        SearchLog.create_date,
        SearchLog.name_search_pattern,
        SearchLog.address_search_pattern,
        SearchLog.n_results,
        SearchLog.index
    ]
    if return_result:
        requested_fields.append(SearchLog.search_result)

    if name_pattern and address_pattern:
        select_condition = or_(
            SearchLog.name_search_pattern.like(f'%{name_pattern}%'),
            SearchLog.address_search_pattern.like(f'%{address_pattern}%'),
            )
    elif name_pattern:
        select_condition = SearchLog.name_search_pattern.like(f'%{name_pattern}%')
    elif address_pattern:
        select_condition = SearchLog.address_search_pattern.like(f'%{address_pattern}%')

    # *tuple(requested_fields)
    query = select(SearchLog.address_search_pattern, SearchLog.n_results, SearchLog.index).where(select_condition)
    res = db.sql_query(query=query)
    logger.info(res)
    return {"message": "success", "data": res} 