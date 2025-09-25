# api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os

# import managers from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.logic import UserManager, FactManager, FavoriteManager

# -------------------------------------- App Setup ---------------------------
app = FastAPI(title="Fun Facts Generator API", version="1.0")

# ------------------------ Allow frontend (streamlit/React) ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------- Data Models -------------------------------
class UserCreate(BaseModel):
    username: str
    email: str

class UserUpdate(BaseModel):
    username: str = None
    email: str = None

class FactCreate(BaseModel):
    content: str
    category: str
    user_id: int = None

class FactUpdate(BaseModel):
    content: str = None
    category: str = None

class FavoriteCreate(BaseModel):
    user_id: int
    fact_id: int

# ------------------------ API Classes ----------------------
class UserAPI:
    def __init__(self):
        self.manager = UserManager()

    def register_routes(self, app: FastAPI):
        @app.post("/users/")
        def create_user(user: UserCreate):
            result = self.manager.add_user(user.username, user.email)
            if result.get("Success"):
                return result
            raise HTTPException(status_code=400, detail=result.get("Message"))

        @app.get("/users/")
        def list_users():
            result = self.manager.list_user()
            return {"success": True, "data": result}

        @app.put("/users/{user_id}")
        def update_user(user_id: int, user: UserUpdate):
            result = self.manager.edit_user(user_id, user.username, user.email)
            if result.get("Success"):
                return result
            raise HTTPException(status_code=400, detail=result.get("Message"))

        @app.delete("/users/{user_id}")
        def delete_user(user_id: int):
            result = self.manager.remove_user(user_id)
            if result.get("Success"):
                return result
            raise HTTPException(status_code=400, detail=result.get("Message"))


class FactAPI:
    def __init__(self):
        self.manager = FactManager()

    def register_routes(self, app: FastAPI):
        @app.post("/facts/")
        def create_fact(fact: FactCreate):
            result = self.manager.add_fact(fact.content, fact.category, fact.user_id)
            if result.get("Success"):
                return result
            raise HTTPException(status_code=400, detail=result.get("Message"))

        @app.get("/facts/")
        def list_facts():
            result = self.manager.list_facts()
            return {"success": True, "data": result}

        @app.put("/facts/{fact_id}")
        def update_fact(fact_id: int, fact: FactUpdate):
            result = self.manager.edit_fact(fact_id, fact.content, fact.category)
            if result.get("Success"):
                return result
            raise HTTPException(status_code=400, detail=result.get("Message"))

        @app.delete("/facts/{fact_id}")
        def delete_fact(fact_id: int):
            result = self.manager.remove_fact(fact_id)
            if result.get("Success"):
                return result
            raise HTTPException(status_code=400, detail=result.get("Message"))

        @app.get("/facts/random/")
        def random_fact(category: str = None):
            result = self.manager.random_fact(category)
            if result.get("Success"):
                return result
            raise HTTPException(status_code=404, detail=result.get("Message"))


class FavoriteAPI:
    def __init__(self):
        self.manager = FavoriteManager()

    def register_routes(self, app: FastAPI):
        @app.post("/favorites/")
        def add_favorite(fav: FavoriteCreate):
            result = self.manager.add_favorite(fav.user_id, fav.fact_id)
            if result.get("Success"):
                return result
            raise HTTPException(status_code=400, detail=result.get("Message"))

        @app.get("/favorites/{user_id}")
        def list_favorites(user_id: int):
            result = self.manager.list_favorites(user_id)
            return {"success": True, "data": result}

        @app.delete("/favorites/{fav_id}")
        def delete_favorite(fav_id: int):
            result = self.manager.remove_favorite(fav_id)
            if result.get("Success"):
                return result
            raise HTTPException(status_code=400, detail=result.get("Message"))

# ------------------------ Register all API classes ----------------------
UserAPI().register_routes(app)
FactAPI().register_routes(app)
FavoriteAPI().register_routes(app)

# ------------------------ Home ----------------------
@app.get("/")
def home():
    return {"message": "Fun Facts Generator API is running!"}

# --------------- run ----------------------------
if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
