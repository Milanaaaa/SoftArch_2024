from fastapi import FastAPI

from config import APP_META

from messages import router as messages_router

app = FastAPI(**APP_META)

app.include_router(messages_router)
