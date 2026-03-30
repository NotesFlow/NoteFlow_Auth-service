from fastapi import FastAPI

app = FastAPI(title="NoteFlow Auth Service")

@app.get("/health")
def health():
    return {"status": "ok"}