from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.responses import get_sector_data_response
from api.settings import get_settings


settings = get_settings()

def create_app() -> FastAPI:
    app = FastAPI()

    return app


app = create_app()

items = [
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"}
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGIN], # Replace with the URL of your web application
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/items")
async def read_items():
    return items

@app.get("/{sector_id}")
async def read_sector(sector_id: int):
    data = get_sector_data_response(sector_id)
    return data