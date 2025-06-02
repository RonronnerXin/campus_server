from sqlmodel import Session

from app.models.user_model import User, UserCreate
from app.core.security import get_password_hash,verify_password

def create_user(session: Session, user_create: UserCreate) -> User:
    hashed_password = get_password_hash(user_create.password)
    user = User(email=user_create.email, hashed_password=hashed_password, username=user_create.username)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_email(session: Session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()

def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
#     user_data = user_in.model_dump(exclude_unset=True)
#     extra_data = {}
#     if "password" in user_data:
#         password = user_data["password"]
#         hashed_password = get_password_hash(password)
#         extra_data["hashed_password"] = hashed_password
#     db_user.sqlmodel_update(user_data, update=extra_data)
#     session.add(db_user)
#     session.commit()
#     session.refresh(db_user)
#     return db_user