from fastapi import Depends, Header, HTTPException

from app.database import get_conn
from app.security import decode_token


def get_current_user(
    authorization: str | None = Header(default=None)
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Login required"
        )


    if not authorization.startswith("Bearer "):

        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header"
        )


    token = authorization.split(
        " ",
        1
    )[1]


    user_id = decode_token(token)


    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


    connection = get_conn()


    user = connection.execute(
        """
        SELECT
            id,
            name,
            email
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()


    connection.close()


    if not user:

        raise HTTPException(
            status_code=401,
            detail="User not found"
        )


    return dict(user)