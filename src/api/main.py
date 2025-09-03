from hmac import new
from fastapi import FastAPI
from .routes.login import router as login
from .routes.health import router as health


app = FastAPI()
app.include_router(login)
app.include_router(health)
app.host = "127.0.0.1"
app.port = 8000

@app.get("/")
async def root():
    return {"message": "Hello World"}