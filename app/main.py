from fastapi import FastAPI
from app.router.web_router import web_router
from app.router.mobile_router import mobile_router

app = FastAPI()

app.include_router(web_router)
app.include_router(mobile_router)
