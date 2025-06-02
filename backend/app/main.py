from fastapi import FastAPI
from fastapi.routing import APIRoute
from sqlmodel import SQLModel
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.api.main import api_router
from app.core.config import settings
from app.core.db import engine


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api_router, prefix='/api')
SQLModel.metadata.create_all(engine)

