from loguru import logger
from fastapi import APIRouter, Depends
from sqlalchemy import select, or_
from sqlalchemy.inspection import inspect
from src.database import get_db
from src.database.db import Database
from src.database.models import SearchLog
from src.search.people_search import PeopleSearch
from src.search import get_search_obj


main_router = APIRouter(prefix="", tags=["search"])


@main_router.get("/search")
async def search_person(
    name="", address="", ps: PeopleSearch = Depends(get_search_obj)
):
    res = ps.search(name, address)
    logger.info(res)
    return {"message": res}


@main_router.get("/history")
async def get_previous_search_results(
    name_pattern="",
    address_pattern="",
    return_results=False,
    db: Database = Depends(get_db),
):
    """This function returns all search requests logged at search_log db table."""
    query = select(SearchLog).where(
        or_(
            SearchLog.name_search_pattern.like(f"%{name_pattern}%"),
            SearchLog.address_search_pattern.like(f"%{address_pattern}%"),
        )
    )
    res = db.sql_query(query=query, single=False)

    # filter sql_query form response
    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

    serialized_res = [object_as_dict(x) for x in res]
    for item in serialized_res:
        del item["search_query"]
        if not return_results:
            del item["search_result"]

    return {"message": "success", "data": serialized_res}
