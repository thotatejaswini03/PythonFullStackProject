# src/logic.py

from src.db import (
    add_user, get_users, get_user_by_email, update_user, delete_user,
    add_fact, get_facts, update_fact, delete_fact, get_random_fact,
    add_favorite, get_user_favorites
)

class UserManager:
    def add_user(self, username, email, password):
        if not username or not email or not password:
            return {"Success": False, "Message": "Username, Email, and Password are required!"}
        result = add_user(username, email, password)
        if result: return {"Success": True, "Message": "User added successfully!", "data": result}
        return {"Success": False, "Message": "Failed to add user"}

    def list_user(self):
        return get_users()

    def get_user_by_email(self, email):
        return get_user_by_email(email)

    def edit_user(self, user_id, username=None, email=None, password=None):
        result = update_user(user_id, username, email, password)
        if result: return {"Success": True, "Message": "User updated successfully!", "data": result}
        return {"Success": False, "Message": "User not found or update failed"}

    def remove_user(self, user_id):
        result = delete_user(user_id)
        if result: return {"Success": True, "Message": "User deleted successfully!"}
        return {"Success": False, "Message": "User not found"}

class FactManager:
    def add_fact(self, content, category, user_id=None):
        if not content or not category:
            return {"Success": False, "Message": "Content and Category are required!"}
        result = add_fact(content, category, user_id)
        if result: return {"Success": True, "Message": "Fact added successfully!", "data": result}
        return {"Success": False, "Message": "Failed to add fact"}

    def list_facts(self):
        return get_facts()

    def edit_fact(self, fact_id, content=None, category=None):
        result = update_fact(fact_id, content, category)
        if result: return {"Success": True, "Message": "Fact updated successfully!", "data": result}
        return {"Success": False, "Message": "Fact not found or update failed"}

    def remove_fact(self, fact_id):
        result = delete_fact(fact_id)
        if result: return {"Success": True, "Message": "Fact deleted successfully!"}
        return {"Success": False, "Message": "Fact not found"}

    def random_fact(self, category=None):
        fact = get_random_fact(category)
        if fact: return {"Success": True, "Fact": fact}
        return {"Success": False, "Message": "No facts found"}

class FavoriteManager:
    def add_to_favorites(self, user_id, fact_id):
        result = add_favorite(user_id, fact_id)
        if result:
            return {"Success": True, "Message": "Added to favorites!"}
        return {"Success": False, "Message": "Already in favorites or invalid"}

    def list_favorites(self, user_id):
        favs = get_user_favorites(user_id)
        favorites = []
        for f in favs:
            fact = f.get("fun_facts")
            if fact:
                favorites.append(fact)
        return favorites