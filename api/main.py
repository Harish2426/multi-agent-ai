from fastapi import FastAPI

from api.routes import router

app = FastAPI(
    title="Multi-Agent AI",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():

    return {
        "message": "Multi-Agent AI API Running"
    }