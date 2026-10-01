from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


ALGORITHM = "HS256"


# ---------------------------------------------------------
# Password
# ---------------------------------------------------------

def hash_password(password: str) -> str:

    return pwd_context.hash(password)


def verify_password(
    password: str,
    hashed_password: str
) -> bool:

    return pwd_context.verify(
        password,
        hashed_password
    )


# ---------------------------------------------------------
# JWT
# ---------------------------------------------------------

def create_access_token(user_id: int):

    expire = (
        datetime.now(timezone.utc)
        +
        timedelta(
            minutes=settings.token_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM
    )


def decode_token(token: str):

    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM]
        )

        return int(payload["sub"])

    except (
        JWTError,
        KeyError,
        ValueError
    ):

        return None