import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routers import user, auth
from app.deps import get_user_info

app = FastAPI()

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 認証不要
app.include_router(auth.router)

# 認証必要
app.include_router(user.router, dependencies=[Depends(get_user_info)])

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI!"}
