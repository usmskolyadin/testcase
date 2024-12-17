from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.v1 import v1

def create_app() -> FastAPI:
    app = FastAPI(
        title="Test case API",
        description="Test case API description",
        version='0.1.0',
        docs_url='/',
        redoc_url='/docs',
    )

    app.include_router(v1)

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=[
            "http://127.0.0.1:5173",
            "http://localhost:5173",
        ],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()
