from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth_utils import get_current_user
from database import get_db
from models import User as DBUser

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
def get_my_user(
    current_user: DBUser = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_in_db = db.query(DBUser).filter(DBUser.id == current_user.id).first()
    return {
        "id": user_in_db.id,
        "email": user_in_db.email,
        "is_active": user_in_db.is_active,
        "created_at": user_in_db.created_at,
        "updated_at": user_in_db.updated_at
    }
