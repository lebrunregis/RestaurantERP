from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.users_model import Users


# --- CRUD Accessors for Users --- #

def create_user(
    db: Session,
    username: str,
    email: Optional[str] = None
) -> Users:
    new_user = Users(
        username=username,
        email=email
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_by_id(db: Session, user_id: int) -> Optional[Users]:
    return db.query(Users).filter(Users.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[Users]:
    return db.query(Users).filter(Users.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[Users]:
    return db.query(Users).filter(Users.email == email).first()


def get_all_users(db: Session) -> List[Users]:
    return db.query(Users).all()


def update_user(
    db: Session,
    user_id: int,
    username: Optional[str] = None,
    email: Optional[str] = None
) -> Optional[Users]:
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        return None
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True