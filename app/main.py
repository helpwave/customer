import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.exc import OperationalError

from routers.contract import router as contract_router
from routers.customer import router as customer_router
from routers.customer_product import router as customer_product_router
from routers.product import router as product_router
from routers.voucher import router as voucher_router
from utils.config import keycloak_openid, settings
from utils.database.connection import engine
from utils.helpers.example import create_example_data
from utils.security.token import TokenResponse, authenticate_user

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

    if settings.DEVELOPMENT:
        create_example_data()

    yield


app = FastAPI(title="helpwave customer", lifespan=lifespan)

app.include_router(customer_router)
app.include_router(product_router)
app.include_router(customer_product_router)
app.include_router(voucher_router)
app.include_router(contract_router)

origins = ["*" if settings.DEVELOPMENT else settings.EXTERNAL_URL]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/callback", response_model=TokenResponse, include_in_schema=False)
async def callback(request: Request):
    keycode = request.query_params.get("code") or ""

    access_token = authenticate_user(keycode, request)

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    return access_token


@app.get("/login", response_class=RedirectResponse, include_in_schema=False)
async def login(request: Request):
    auth_url = keycloak_openid.auth_url(
        redirect_uri=str(request.url_for("callback")),
        scope="openid profile email",
    )

    return RedirectResponse(auth_url)
