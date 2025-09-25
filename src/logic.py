# src/logic.py

from src.db import DatabaseManager

# ----------------- USERS -----------------
class UserManager:
    """
    Handles CRUD operations for the users table
    """
    def __init__(self):
        self.db = DatabaseManager()

    def add_user(self, username, email):
        if not username or not email:
            return {"Success": False, "Message": "username and email are required"}
        result = self.db.add_user(username, email)
        if result:
            return {"Success": True, "Message": "User added successfully!", "data": result}
        return {"Success": False, "Message": "Failed to add user"}

    def list_user(self):
        return self.db.get_users()

    def edit_user(self, user_id, username=None, email=None):
        result = self.db.update_user(user_id, username, email)
        if result:
            return {"Success": True, "Message": "User updated successfully!", "data": result}
        return {"Success": False, "Message": "User not found or update failed"}

    def remove_user(self, user_id):
        result = self.db.delete_user(user_id)
        if result:
            return {"Success": True, "Message": "User deleted successfully!"}
        return {"Success": False, "Message": "User not found"}


# ----------------- FACTS -----------------
class FactManager:
    """
    Handles CRUD operations for the facts table
    """
    def __init__(self):
        self.db = DatabaseManager()

    def add_fact(self, content, category, user_id=None):
        if not content or not category:
            return {"Success": False, "Message": "content and category are required"}
        result = self.db.add_fact(content, category, user_id)
        if result:
            return {"Success": True, "Message": "Fact added successfully!", "data": result}
        return {"Success": False, "Message": "Failed to add fact"}

    def list_facts(self):
        return self.db.get_facts()

    def edit_fact(self, fact_id, content=None, category=None):
        result = self.db.update_fact(fact_id, content, category)
        if result:
            return {"Success": True, "Message": "Fact updated successfully!", "data": result}
        return {"Success": False, "Message": "Fact not found or update failed"}

    def remove_fact(self, fact_id):
        result = self.db.delete_fact(fact_id)
        if result:
            return {"Success": True, "Message": "Fact deleted successfully!"}
        return {"Success": False, "Message": "Fact not found"}

    def random_fact(self, category=None):
        result = self.db.get_random_fact(category)
        if result:
            return {"Success": True, "Fact": result}
        return {"Success": False, "Message": "No facts found"}


# ----------------- FAVORITES -----------------
class FavoriteManager:
    """
    Handles CRUD operations for the favorites table
    """
    def __init__(self):
        self.db = DatabaseManager()

    def add_favorite(self, user_id, fact_id):
        if not user_id or not fact_id:
            return {"Success": False, "Message": "user_id and fact_id are required"}
        result = self.db.add_favorite(user_id, fact_id)
        if result:
            return {"Success": True, "Message": "Favorite added successfully!", "data": result}
        return {"Success": False, "Message": "Failed to add favorite"}

    def list_favorites(self, user_id):
        return self.db.get_favorites(user_id)

    def remove_favorite(self, fav_id):
        result = self.db.delete_favorite(fav_id)
        if result:
            return {"Success": True, "Message": "Favorite removed successfully!"}
        return {"Success": False, "Message": "Favorite not found"}
