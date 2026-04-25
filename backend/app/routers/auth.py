from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.user import get_user_by_email
from app.services.auth import verify_password, create_access_token
from app.deps import get_db, get_user_info

router = APIRouter()

@router.post("/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="メールアドレスまたはパスワードが正しくありません")
    token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
    )
    return TokenResponse(access_token=token)

@router.get("/auth/user")
async def get_auth_user(current_user=Depends(get_user_info)):
    return {"id": current_user.id, "email": current_user.email}

@router.post("/auth/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "ログアウトしました"}
