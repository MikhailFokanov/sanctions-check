import uvicorn

from fastapi import FastAPI
from loguru import logger

from src.database.models import Base
from src.database import get_db
from src.router import main_router


db = get_db()
app = FastAPI()
app.include_router(main_router)


@app.middleware("lifespan")
async def lifespan_middleware(request, call_next):
    print("Lifespan event handling")
    try:
        logger.info("Application starting up...")
        db.connect()
        db.create_tables(Base)

        response = await call_next(request)

        logger.info("Application shutting down...")
        db.disconnect()

        return response
    except Exception as e:
        logger.exception(f"Error during lifespan event: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
    #main()

