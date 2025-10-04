# src/db.py

import os
import random
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- USERS ----------------
def add_user(username, email, password_hash):
    return supabase.table("usersdata").insert({
        "username": username,
        "email": email,
        "password_hash": password_hash
    }).execute().data

def get_users():
    return supabase.table("usersdata").select("*").execute().data

def get_user_by_email(email):
    users = supabase.table("usersdata").select("*").eq("email", email).execute().data
    return users[0] if users else None

def update_user(user_id, username=None, email=None, password_hash=None):
    data = {}
    if username: data["username"] = username
    if email: data["email"] = email
    if password_hash: data["password_hash"] = password_hash
    return supabase.table("usersdata").update(data).eq("id", user_id).execute().data

def delete_user(user_id):
    return supabase.table("usersdata").delete().eq("id", user_id).execute().data

# ---------------- FACTS ----------------
def add_fact(content, category, user_id=None):
    data = {"fact_text": content, "category": category}
    if user_id: data["created_by"] = user_id
    return supabase.table("fun_facts").insert(data).execute().data

def get_facts():
    return supabase.table("fun_facts").select("*").execute().data

def update_fact(fact_id, content=None, category=None):
    data = {}
    if content: data["fact_text"] = content
    if category: data["category"] = category
    return supabase.table("fun_facts").update(data).eq("id", fact_id).execute().data

def delete_fact(fact_id):
    return supabase.table("fun_facts").delete().eq("id", fact_id).execute().data

def get_random_fact(category=None):
    q = supabase.table("fun_facts").select("*")
    if category: q = q.eq("category", category)
    facts = q.execute().data
    return random.choice(facts) if facts else None

# ---------------- FAVORITES ----------------
def add_favorite(user_id, fact_id):
    # Check if already favorited
    exists = supabase.table("user_favorites").select("*") \
        .eq("user_id", user_id).eq("fact_id", fact_id).execute().data
    if exists:
        return None
    return supabase.table("user_favorites").insert({
        "user_id": user_id,
        "fact_id": fact_id
    }).execute().data

def get_user_favorites(user_id):
    res = supabase.table("user_favorites").select("fact_id, fun_facts(*)") \
        .eq("user_id", user_id).execute().data
    return res