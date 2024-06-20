from fastapi import FastAPI
from app.routers import chat
from fastapi.middleware.cors import CORSMiddleware
                      
                         
VERSION = "1.0.0"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [chat]

for item in routers:
    app.include_router(item.router)


@app.get("/", tags=["Index"])
def read_root():
    return {"version": VERSION}
