from database_api.db.models import Base
from database_api.router import users 
from database_api.db.database import engine
from fastapi import FastAPI
Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(users.router)
