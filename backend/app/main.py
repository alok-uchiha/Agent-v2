from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware


from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.dependency import get_db
from backend.app.api.routes import auth, user,chat


app=FastAPI()


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(chat.router)

@app.get("/")
def hello():
    return {
        "message":"hello fellows"
    }

@app.get("/test-db")
async def test_db(db: AsyncSession = Depends(get_db)):
    return {"message": "Database connected"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your real domain later
    allow_methods=["*"],
    allow_headers=["*"],
)