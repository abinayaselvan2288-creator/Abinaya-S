from fastapi import APIRouter, Depends, HTTPException

from app.schemas import (
    RegisterRequest,
    LoginRequest
)

from app.database import get_conn

from app.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.dependencies import get_current_user


router = APIRouter(
    tags=["Authentication"]
)


# ---------------------------------------------------------
# REGISTER
# ---------------------------------------------------------

@router.post("/register")
def register(data: RegisterRequest):

    connection = get_conn()

    try:

        connection.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                data.name.strip(),
                data.email.lower().strip(),
                hash_password(data.password)
            )
        )

        connection.commit()

        user_id = connection.execute(
            "SELECT last_insert_rowid()"
        ).fetchone()[0]

    except Exception as e:

        connection.close()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    connection.close()

    return {
        "access_token": create_access_token(user_id),
        "token_type": "bearer"
    }


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------

@router.post("/login")
def login(data: LoginRequest):

    connection = get_conn()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (
            data.email.lower().strip(),
        )
    ).fetchone()

    connection.close()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        data.password,
        user["password_hash"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token":
            create_access_token(user["id"]),

        "token_type":
            "bearer"
    }

