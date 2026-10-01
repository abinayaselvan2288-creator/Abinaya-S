import json

from fastapi import (
    APIRouter,
    Depends
)

from app.dependencies import get_current_user
from app.database import get_conn


router = APIRouter(
    tags=["History"]
)


@router.get("/history")
def history(
    user=Depends(get_current_user)
):

    connection = get_conn()


    rows = connection.execute(
        """
        SELECT
            id,
            planner,
            request_json,
            response_json,
            created_at

        FROM recommendations

        WHERE user_id = ?

        ORDER BY id DESC

        LIMIT 30
        """,
        (
            user["id"],
        )
    ).fetchall()


    connection.close()


    return [

        {
            "id": row["id"],

            "planner":
                row["planner"],

            "request":
                json.loads(
                    row["request_json"]
                ),

            "response":
                json.loads(
                    row["response_json"]
                ),

            "created_at":
                row["created_at"]
        }

        for row in rows
    ]