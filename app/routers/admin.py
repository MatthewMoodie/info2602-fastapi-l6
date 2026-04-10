from fastapi import APIRouter, Request, Query
from sqlmodel import select, func
from app.database import SessionDep
from app.models import Todo, User
from app.auth import AdminDep
from app.main import templates
from app.pagination import Pagination

admin_router = APIRouter(tags=["Admin App"])

@admin_router.get("/admin")
def admin_page(
    request: Request, 
    db: SessionDep, 
    user: AdminDep, 
    page: int = Query(default=1, ge=1), 
    limit: int = Query(default=100, le=100), 
    q: str = Query(default=''), 
    done: str = Query(default="any")):
    
    offset = (page - 1) * limit

    db_qry = select(Todo).join(User)
    
    # Advanced Querying (Search)
    if q:
        db_qry = db_qry.where(
            Todo.text.ilike(f"%{q}%") | User.username.ilike(f"%{q}%")
        )
        
    # Filtering
    if done == "true": 
        db_qry = db_qry.where(Todo.done == True)
    elif done == "false": 
        db_qry = db_qry.where(Todo.done == False)
        
    count_qry = select(func.count()).select_from(db_qry.subquery())
    count_todos = db.exec(count_qry).one()

    todos = db.exec(db_qry.offset(offset).limit(limit)).all()
    pagination = Pagination(total_count=count_todos, current_page=page, limit=limit)

    return templates.TemplateResponse(
        request=request, 
        name="admin.html",
        context={
            "current_user": user,
            "todos": todos,
            "pagination": pagination,
            "q": q,
            "done": done
        }
    )