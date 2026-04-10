from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from app.auth import AuthDep, is_logged_in, get_current_user, is_admin
from app.main import templates
from typing import Annotated
from app.database import SessionDep

IsUserLoggedIn = Annotated[bool, Depends(is_logged_in)]

home_router = APIRouter()

@home_router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    user_logged_in: IsUserLoggedIn,
    db: SessionDep):
    if user_logged_in:
        user = await get_current_user(request, db)
        if await is_admin(user):
            return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
        return RedirectResponse(url="/app", status_code=status.HTTP_303_SEE_OTHER)
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@home_router.get("/app", response_class=HTMLResponse)
async def app_dashbaord(
    request: Request,
    user: AuthDep):
    return templates.TemplateResponse(
        request=request, 
        name="todo.html",
        context={
            "current_user": user
        }
    )