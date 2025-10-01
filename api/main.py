# api/main.py

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from src.logic import UserManager, FactManager
from src.db import supabase

app = FastAPI(title="Fun Facts Generator API", version="1.0")

# -------------------- Data Models --------------------
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class FactCreate(BaseModel):
    content: str
    category: str
    user_id: str = None

class FactUpdate(BaseModel):
    content: str = None
    category: str = None

# -------------------- Managers --------------------
user_manager = UserManager()
fact_manager = FactManager()

# -------------------- Auth Endpoints --------------------
@app.post("/auth/register/")
def register(user: UserRegister):
    result = user_manager.add_user(user.username, user.email, password=user.password)
    if result.get("Success"):
        return result
    raise HTTPException(status_code=400, detail=result.get("Message"))

@app.post("/auth/login/")
def login(user: UserLogin):
    db_user_list = user_manager.list_user()
    db_user = next((u for u in db_user_list if u["email"] == user.email), None)
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if db_user["password_hash"] == user.password:
        return {"Success": True, "Message": f"Welcome {db_user['username']}", "user_id": db_user["id"]}

    raise HTTPException(status_code=401, detail="Incorrect password")

# -------------------- User Endpoints --------------------
@app.get("/users/")
def list_users():
    return {"success": True, "data": user_manager.list_user()}

@app.put("/users/{user_id}")
def update_user(user_id: str, username: str = None, email: str = None, password: str = None):
    result = user_manager.edit_user(user_id, username, email, password)
    if result.get("Success"):
        return result
    raise HTTPException(status_code=400, detail=result.get("Message"))

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    result = user_manager.remove_user(user_id)
    if result.get("Success"):
        return result
    raise HTTPException(status_code=400, detail=result.get("Message"))

# -------------------- Fact Endpoints --------------------
@app.post("/facts/")
def create_fact(fact: FactCreate):
    result = fact_manager.add_fact(fact.content, fact.category, fact.user_id)
    if result.get("Success"):
        return result
    raise HTTPException(status_code=400, detail=result.get("Message"))

@app.get("/facts/")
def list_facts():
    return {"success": True, "data": fact_manager.list_facts()}

@app.put("/facts/{fact_id}")
def update_fact(fact_id: str, fact: FactUpdate):
    result = fact_manager.edit_fact(fact_id, fact.content, fact.category)
    if result.get("Success"):
        return result
    raise HTTPException(status_code=400, detail=result.get("Message"))

@app.delete("/facts/{fact_id}")
def delete_fact(fact_id: str):
    result = fact_manager.remove_fact(fact_id)
    if result.get("Success"):
        return result
    raise HTTPException(status_code=400, detail=result.get("Message"))

@app.get("/facts/random/")
def random_fact(category: str = None):
    result = fact_manager.random_fact(category)
    if result.get("Success"):
        return result
    raise HTTPException(status_code=404, detail=result.get("Message"))

# -------------------- Favorites Endpoints --------------------
@app.post("/favorites/add/")
def add_favorite(payload: dict = Body(...)):
    user_id = payload.get("user_id")
    fact_id = payload.get("fact_id")
    if not user_id or not fact_id:
        raise HTTPException(status_code=400, detail="user_id and fact_id are required")

    # Check duplicate
    existing = supabase.table("user_favorites").select("*") \
        .eq("user_id", user_id).eq("fact_id", fact_id).execute().data
    if existing:
        return {"Success": True, "Message": "Already in favorites"}

    try:
        supabase.table("user_favorites").insert({
            "user_id": user_id,
            "fact_id": fact_id
        }).execute()
        return {"Success": True, "Message": "Added to favorites!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/favorites/{user_id}")
def get_favorites(user_id: str):
    try:
        response = supabase.table("user_favorites") \
            .select("*, fun_facts(*)") \
            .eq("user_id", user_id).execute()

        favorites = []
        if response.data:
            for fav in response.data:
                fact = fav.get("fun_facts")
                if fact:
                    favorites.append({
                        "id": fact["id"],
                        "fact_text": fact["fact_text"],
                        "category": fact.get("category", "")
                    })
        return {"favorites": favorites}
    except Exception as e:
        return {"favorites": [], "error": str(e)}

# -------------------- Home --------------------
@app.get("/")
def home():
    return {"message": "Fun Facts Generator API is running!"}
