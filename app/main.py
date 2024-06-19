from fastapi import FastAPI

VERSION = "1.0.0"

app = FastAPI()


@app.get("/", tags=["Information"])
def read_root():
    return {"version": VERSION}
