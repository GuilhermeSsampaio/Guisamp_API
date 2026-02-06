from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.db import create_db_and_tables
from auth.models.user import User
from auth.models.auth_provider import AuthProvider
from auth.routes.auth_routes import router as auth_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(title="API unificada para projetos pessoais - GuiSamp",
              version="2.0",
              lifespan=lifespan
              )

# mudar pra produção esses valores
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"]
)

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"Bem vindo": "GuiSamp api"}

