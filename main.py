import uvicorn

from fastapi import FastAPI
from loguru import logger

from src.database import get_db
from src.router import main_router


db = get_db()
app = FastAPI()
app.include_router(main_router)


if __name__ == "__main__":
    try: 
        logger.info("Application starting up...")
        uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
    except Exception as e:
        logger.exception(e)
    finally:
        db.disconnect()

