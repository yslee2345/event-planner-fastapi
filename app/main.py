import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.events import event_router
from routes.users import user_router
from app.models.events import Event

app = FastAPI()
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def on_startup():
    ...


if __name__ == '__main__':
    uvicorn.run("main:app",host="127.0.0.1", port=8080, reload=True, workers=1)