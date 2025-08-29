from hmac import new
from fastapi import FastAPI
from .routes.login import router as login
from .routes.health import router as health


app = FastAPI()
app.include_router(login)
app.include_router(health)

@app.get("/")
async def root():
    return {"message": "Hello World"}