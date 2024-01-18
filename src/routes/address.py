from datetime import datetime, date
from sqlalchemy.orm import Session
from pydantic import BaseModel
from . import get_db
from loguru import logger
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi import FastAPI, HTTPException
from src.db.models import Address
router = APIRouter()


app = FastAPI()

class UserAddressCreate(BaseModel):
    u_id:int
    user_address: str
    is_deleted: int


@router.post("/Address/add")
def add_users(
        user: UserAddressCreate,
        db: Session = Depends(get_db)
):
    try:
        user = Address(
            u_id=user.u_id,
            user_address=user.user_address,
            is_deleted=0
        )
        db.add(user)
        db.commit()
        return {"message": "User address added successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/Address/{u_id}")
def get_usersAddr_By_Uid(
        u_id: int,
        db: Session = Depends(get_db)
):
    try:
        users = db.query(Address).filter_by(u_id=u_id).all()
        if len(users) == 0:
            raise HTTPException(status_code=404, detail=f"Users not found for id: {u_id}")
        return users
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/Address/{a_id}")
def get_usersAddr_By_Aid(
        a_id: int,
        db: Session = Depends(get_db)
):
    try:
        users = db.query(Address).filter_by(u_id=a_id).all()
        if len(users) == 0:
            raise HTTPException(status_code=404, detail=f"Users not found for id: {a_id}")
        return users
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.put("/Address/modify/{a_id}")
def modify_usersAddress_info(
        user_modify: UserAddressCreate,
        id: int,
        db: Session = Depends(get_db)
):
    try:
        # Check if User Exists:
        res_user = db.query(Address).filter_by(a_id=id).all()
        if len(res_user) == 0:
            raise HTTPException(status_code=404, detail=f"Users not found for id: {id}")

        # Update User Info:
        user_modify = user_modify.dict(exclude_unset=True)
        db.query(Address).filter_by(a_id=id).update(user_modify)
        db.commit()
        return {"message": "User Address updated successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/Address/delete/{a_id}")
def delete_userAddr_by_a_id(
        id: int,
        db: Session = Depends(get_db)
):
    try:
        # Check if User Exists:
        res_user = db.query(Address).filter_by(a_id=id).all()
        if len(res_user) == 0:
            raise HTTPException(status_code=404, detail=f"Users not found for id: {id}")

        # Delete User:
        db.query(Address).filter_by(a_id=id).delete()
        db.commit()
        return {"message": "User deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")