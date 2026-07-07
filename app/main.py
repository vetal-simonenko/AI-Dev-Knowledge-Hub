from fastapi import FastAPI

app = FastAPI(title="AI Dev Knowledge Hub")


@app.get("/health")
def health_check():
    return {"status": "ok"}