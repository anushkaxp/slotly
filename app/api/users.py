
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse


from app.core.security import verify_password
from app.core.tokens import create_access_token
from app.schemas.user import UserLogin, TokenResponse

from app.api.dependencies import get_current_user


router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = db.scalar(
        select(User).where(User.email == str(payload.email).lower())
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    user = User(
        name=payload.name,
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
        phone=payload.phone,
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        )

    return user





@router.post("/login", response_model=TokenResponse)
def login_user(
    payload: UserLogin,
    db: Session = Depends(get_db),
):
    email = str(payload.email).lower()

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if not user or not verify_password(
        payload.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }



@router.get("/me", response_model=UserResponse)
def read_current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user






# Why check twice? The initial query gives a friendly error for an existing email. The database's unique 
# constraint protectsagainst two simultaneous requests registering the same email. 
# The IntegrityError handler catches that race.


