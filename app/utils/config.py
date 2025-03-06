from keycloak import KeycloakOpenID
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEVELOPMENT: bool = Field(env="DEVELOPMENT", default=False)
    LOG_LEVEL: str = Field(env="LOG_LEVEL", default="INFO")
    EXTERNAL_URL: str = Field(
        env="EXTERNAL_URL", default="https://api.customer.helpwave.de"
    )

    DATABASE_HOSTNAME: str = Field(env="DATABASE_HOSTNAME", default="postgres")
    DATABASE_NAME: str = Field(env="DATABASE_NAME", default="customer")
    DATABASE_USERNAME: str = Field(env="DATABASE_USERNAME", default="customer")
    DATABASE_PASSWORD: str = Field(env="DATABASE_PASSWORD", default="customer")
    DATABASE_PORT: int = Field(env="DATABASE_PORT", default=5432)

    KEYCLOAK_SERVER_URL: str = Field(env="KEYCLOAK_SERVER_URL", default="https://id.helpwave.de")
    KEYCLOAK_REALM: str = Field(env="KEYCLOAK_REALM", default="customer-api-realm")
    KEYCLOAK_CLIENT_ID: str = Field(env="KEYCLOAK_CLIENT_ID", default="customer-api-keycloak")
    KEYCLOAK_CLIENT_SECRET: str = Field(env="KEYCLOAK_CLIENT_SECRET", default="customer-api-client-secret")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    realm_name=settings.KEYCLOAK_REALM,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
)


def get_openid_config():
    return keycloak_openid.well_known()
