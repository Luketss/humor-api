# routes.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from database import get_session
from models import UserSchema, HumorSchema

# Create a router instance
router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.post("/users/")
def create_user(users: UserSchema, session: SessionDep) -> UserSchema:
    session.add(users)
    session.commit()
    session.refresh(users)
    return users


@router.get("/users/")
def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[UserSchema]:
    users = session.exec(select(UserSchema).offset(offset).limit(limit)).all()
    return users


@router.get("/user/{user_id}")
def read_user(user_id: int, session: SessionDep) -> UserSchema:
    user = session.get(UserSchema, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.delete("/user/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(UserSchema, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    session.delete(user)
    session.commit()
    return {"ok": True}


# Routes for HumorSchema
@router.post("/humor/")
def create_humor(humor: HumorSchema, session: SessionDep) -> HumorSchema:
    session.add(humor)
    session.commit()
    session.refresh(humor)
    return humor


@router.get("/humor/")
def read_humor(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[HumorSchema]:
    humors = session.exec(select(HumorSchema).offset(offset).limit(limit)).all()
    return humors


@router.get("/humor/{humor_id}")
def read_humor_by_id(humor_id: int, session: SessionDep) -> HumorSchema:
    humor = session.get(HumorSchema, humor_id)
    if not humor:
        raise HTTPException(status_code=404, detail="Humor entry not found")
    return humor


@router.delete("/humor/{humor_id}")
def delete_humor(humor_id: int, session: SessionDep):
    humor = session.get(HumorSchema, humor_id)
    if not humor:
        raise HTTPException(status_code=404, detail="Humor entry not found")
    session.delete(humor)
    session.commit()
    return {"ok": True}
