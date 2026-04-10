from fastapi import APIRouter

main_router = APIRouter()

from .auth import auth_router
main_router.include_router(auth_router)

from .todo import todo_router
main_router.include_router(todo_router)

from .admin import admin_router
main_router.include_router(admin_router)

from .stats import stats_router
main_router.include_router(stats_router)