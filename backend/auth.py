import os
import secrets

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials


load_dotenv()

security = HTTPBasic()

APP_USERNAME = os.getenv("APP_USERNAME")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def authenticate_user(
    credentials: HTTPBasicCredentials = Depends(security),
):
    if not APP_USERNAME or not APP_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication credentials are not configured.",
        )

    username_ok = secrets.compare_digest(
        credentials.username,
        APP_USERNAME,
    )

    password_ok = secrets.compare_digest(
        credentials.password,
        APP_PASSWORD,
    )

    if not (username_ok and password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username
