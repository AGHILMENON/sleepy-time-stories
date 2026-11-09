from fastapi import FastAPI

app = FastAPI(title="Sleepy Time Stories - Agent API")

@app.get("/healthz")
def healthz():
    return {"ok": True}