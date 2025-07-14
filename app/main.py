from fastapi import FastAPI
from langsmith import tracing_context


from app.core.config.logging import setup_logging
from app.api.main import main_router
from app.core.config.config import settings

app = FastAPI()

setup_logging()



@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(main_router, prefix=settings.API_V1_STR)