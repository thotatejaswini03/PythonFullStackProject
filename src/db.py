# db.py

import os, random
from supabase import create_client
from dotenv import load_dotenv

# Load environment
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# ---------------- USERS ----------------
def add_user(username, email):
    return supabase.table("users").insert({"username": username, "email": email}).execute().data

def get_users():
    return supabase.table("users").select("*").execute().data

def update_user(user_id, username=None, email=None):
    data = {}
    if username: data["username"] = username
    if email: data["email"] = email
    return supabase.table("users").update(data).eq("id", user_id).execute().data

def delete_user(user_id):
    return supabase.table("users").delete().eq("id", user_id).execute().data


# ---------------- FACTS ----------------
def add_fact(content, category, user_id=None):
    data = {"content": content, "category": category}
    if user_id: data["user_id"] = user_id
    return supabase.table("facts").insert(data).execute().data

def get_facts():
    return supabase.table("facts").select("*").execute().data

def update_fact(fact_id, content=None, category=None):
    data = {}
    if content: data["content"] = content
    if category: data["category"] = category
    return supabase.table("facts").update(data).eq("id", fact_id).execute().data

def delete_fact(fact_id):
    return supabase.table("facts").delete().eq("id", fact_id).execute().data

def get_random_fact(category=None):
    q = supabase.table("facts").select("*")
    if category: q = q.eq("category", category)
    facts = q.execute().data
    return random.choice(facts) if facts else None


# ---------------- FAVORITES ----------------
def add_favorite(user_id, fact_id):
    return supabase.table("favorites").insert({"user_id": user_id, "fact_id": fact_id}).execute().data

def get_favorites(user_id):
    return supabase.table("favorites").select("*").eq("user_id", user_id).execute().data

def delete_favorite(fav_id):
    return supabase.table("favorites").delete().eq("id", fav_id).execute().data
