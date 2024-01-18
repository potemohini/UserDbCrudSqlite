from datetime import datetime, date
from sqlalchemy.orm import Session
from pydantic import BaseModel
from . import get_db
from loguru import logger
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi import FastAPI, HTTPException
from src.db.models import Users
router = APIRouter()


app = FastAPI()

class UserCreate(BaseModel):
    user_name: str
    user_dob: date
    is_deleted: int



class UserResponse(UserCreate):
    u_id: int
    is_deleted: bool


@router.post("/Users/add")
def add_users(
        user: UserCreate,
        db: Session = Depends(get_db)
):
    try:
        user = Users(
            user_name=user.user_name,
            user_dob=datetime.now(),
            is_deleted=0
        )
        db.add(user)
        db.commit()
        return {"message": "User added successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/Users/all")
def get_users_list(db: Session = Depends(get_db)):
    try:
        users = db.query(Users).all()
        if len(users) == 0:
            raise HTTPException(status_code=404, detail="Users not found")
        return users
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
@router.get("/Users/{id}")
def get_users_By_Uid(
        u_id: int,
        db: Session = Depends(get_db)
):
    try:
        users = db.query(Users).filter_by(u_id=u_id).all()
        if len(users) == 0:
            raise HTTPException(status_code=404, detail=f"Users not found for id: {u_id}")
        return users
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/Users/modify/{id}")
def modify_users_info(
        user_modify: UserCreate,
        id: int,
        db: Session = Depends(get_db)
):
    try:
        # Check if User Exists:
        res_user = db.query(Users).filter_by(u_id=id).all()
        if len(res_user) == 0:
            raise HTTPException(status_code=404, detail=f"Users not found for id: {id}")

        # Update User Info:
        user_modify = user_modify.dict(exclude_unset=True)
        db.query(Users).filter_by(u_id=id).update(user_modify)
        db.commit()
        return {"message": "User updated successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/Users/delete/{id}")
def delete_user_by_a_id(
        u_id: int,
        db: Session = Depends(get_db)
):
    try:
        # Check if User Exists:
        res_user = db.query(Users).filter_by(u_id=u_id).all()
        if len(res_user) == 0:
            raise HTTPException(status_code=404, detail=f"Users not found for id: {u_id}")

        # Delete User:
        db.query(Users).filter_by(u_id=u_id).delete()
        db.commit()
        return {"message": "User deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")