from fastapi import FastAPI

from app.api.router import router

app = FastAPI(title="AI Dev Knowledge Hub")


@app.get("/")
def root():
    return {"message": "AI Dev Knowledge Hub API"}


app.include_router(router)