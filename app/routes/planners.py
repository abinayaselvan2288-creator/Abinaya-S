import json
import tempfile

from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException
)

from app.dependencies import get_current_user

from app.schemas import (
    HomeRequest,
    PartyRequest
)

from app.services.gemini_service import (
    gemini_service
)

from app.database import get_conn


router = APIRouter(
    tags=["Planners"]
)


# ---------------------------------------------------------
# SAVE HISTORY
# ---------------------------------------------------------

def save_history(
    user_id,
    planner,
    request_data,
    response
):

    connection = get_conn()

    connection.execute(
        """
        INSERT INTO recommendations
        (
            user_id,
            planner,
            request_json,
            response_json
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            planner,
            json.dumps(request_data),
            json.dumps(response)
        )
    )

    connection.commit()

    connection.close()


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------
@router.post("/generate-home")
async def generate_home(
    request: HomeRequest,
    user=Depends(get_current_user)
):
    print("DEBUG: generate_home called")

    request_data = request.model_dump()

    print("REQUEST DATA:", request_data)

    result = gemini_service.generate(
        "home",
        request_data
    )


    save_history(
        user["id"],
        "home",
        request_data,
        result
    )


    return result


# ---------------------------------------------------------
# PARTY
# ---------------------------------------------------------

@router.post("/generate-party")
def generate_party(
    data: PartyRequest,
    user=Depends(get_current_user)
):

    request_data = data.model_dump()

    result = gemini_service.generate(
        "party",
        request_data
    )


    save_history(
        user["id"],
        "party",
        request_data,
        result
    )


    return result


# ---------------------------------------------------------
# JEWELRY
# ---------------------------------------------------------

@router.post("/generate-jewelry")
async def generate_jewelry(

    budget: float = Form(...),

    occasion: str = Form(...),

    style: str = Form("Elegant"),

    outfit_color: str = Form(""),

    outfit_description: str = Form(""),

    outfit_image: UploadFile | None = File(
        default=None
    ),

    user=Depends(get_current_user)
):

    if budget <= 0:

        raise HTTPException(
            status_code=422,
            detail="Budget must be positive"
        )


    image_path = None


    # -----------------------------------------------------
    # IMAGE VALIDATION
    # -----------------------------------------------------

    if outfit_image:

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }


        if outfit_image.content_type not in allowed_types:

            raise HTTPException(
                status_code=400,
                detail="Use JPG, PNG or WEBP"
            )


        suffix = Path(
            outfit_image.filename or ".jpg"
        ).suffix or ".jpg"


        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as file:

            file.write(
                await outfit_image.read()
            )

            image_path = file.name


    # -----------------------------------------------------
    # REQUEST DATA
    # -----------------------------------------------------

    request_data = {

        "budget": budget,

        "occasion": occasion,

        "style": style,

        "outfit_color": outfit_color,

        "outfit_description":
            outfit_description
    }


    # -----------------------------------------------------
    # AI
    # -----------------------------------------------------

    result = gemini_service.generate(
        "jewelry",
        request_data,
        image_path
    )


    # -----------------------------------------------------
    # SAVE
    # -----------------------------------------------------

    save_history(
        user["id"],
        "jewelry",
        request_data,
        result
    )


    # -----------------------------------------------------
    # DELETE TEMP IMAGE
    # -----------------------------------------------------

    if image_path:

        Path(image_path).unlink(
            missing_ok=True
        )


    return result