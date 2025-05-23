from uuid import UUID as UUID4

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakPostError
from pydantic import BaseModel

from models.user import User
from utils.config import keycloak_openid
from utils.database.session import get_database

bearer_scheme = HTTPBearer()


class UserInfo(BaseModel):
    uuid: UUID4

    username: str

    email: str | None = None
    email_verified: bool = False

    fullname: str | None = None
    firstname: str | None = None
    lastname: str | None = None


def verify(token: str) -> UserInfo:
    try:
        user_info = keycloak_openid.userinfo(token)

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        return UserInfo(
            uuid=user_info["sub"],
            username=user_info["preferred_username"],
            email=user_info.get("email"),
            email_verified=user_info.get("email_verified") or False,
            fullname=user_info.get("name"),
            firstname=user_info.get("given_name"),
            lastname=user_info.get("family_name"),
        )
    except KeycloakAuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )


def get_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session=Depends(get_database),
) -> UserInfo:
    token = credentials.credentials

    user_info = verify(token)

    if not user_info.email_verified:
        raise HTTPException(403, detail="Verify email first")

    user = session.query(User).filter_by(uuid=user_info.uuid).first()

    if not user:
        user = User(
            uuid=user_info.uuid,
            name=user_info.fullname,
            email=user_info.email)

        session.add(user)
        session.commit()
        session.refresh(user)

    return user


def authenticate_user(keycode: str, request: Request) -> str:
    try:
        token = keycloak_openid.token(
            grant_type="authorization_code",
            code=keycode,
            redirect_uri=str(request.url_for("callback")),
            scope="openid profile email",
        )
        return token["access_token"]
    except KeycloakAuthenticationError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Login",
        ) from exc
    except KeycloakPostError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Grant",
        ) from exc
