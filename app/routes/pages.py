from fastapi import (
    APIRouter,
    Request
)

from fastapi.responses import HTMLResponse

from fastapi.templating import (
    Jinja2Templates
)


router = APIRouter()


templates = Jinja2Templates(
    directory="app/templates"
)


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# ---------------------------------------------------------
# APPLICATION
# ---------------------------------------------------------

@router.get(
    "/app",
    response_class=HTMLResponse
)
def application(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="app.html"
    )