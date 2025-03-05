import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from routers.customer import router as customer_router
from routers.product import router as product_router
from utils.config import settings
from utils.database.connection import engine

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(meenginessage)s",
    level=settings.LOG_LEVEL,
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        engine.connect()
    except OperationalError:
        logging.error("Connection to database failed.")
        raise RuntimeError("Shutdown, database connection failed.")
    finally:
        yield


app = FastAPI(title="helpwave customer", lifespan=lifespan)

app.include_router(customer_router)
app.include_router(product_router)

origins = ["*" if settings.DEVELOPMENT else settings.EXTERNAL_URL]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
