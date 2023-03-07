from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from starlette.middleware.cors import CORSMiddleware

from api import players_api, teams_api
from db.database import engine

origins = ["http://localhost:3000", ]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(players_api.router)
app.include_router(teams_api.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


def drop_db():
    SQLModel.metadata.drop_all(engine)


def create_db():
    SQLModel.metadata.create_all(engine)


def recreate_db():
    drop_db()
    create_db()
