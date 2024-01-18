import time
from os import environ
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from uvicorn import run
# from loguru import logger
from fastapi import FastAPI
from src.db.models import init_db
from src.routes.all_routes import router

app = FastAPI(title="Test-API")

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


@app.on_event("startup")
async def init_processes():
    environ["PROCESS_START"] = str(int(time.time()))

    if init_db():
        logger.info("DB initialized")
    else:
        pass

    # todo add init cloud mqtt here


if __name__ == '__main__':
    logger.info("Started main")
    run("main:app", host="0.0.0.0", port=5001, reload=True)