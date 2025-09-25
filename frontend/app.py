# app.py

import streamlit as st
import requests

BASE_URL = "http://localhost:8000"  # Your FastAPI backend

st.set_page_config(page_title="Fun Facts Generator", layout="wide")
st.title("🎉 Fun Facts Generator")

# ------------------ Sidebar Navigation ------------------
menu = ["Users", "Facts", "Random Fact", "Favorites"]
choice = st.sidebar.selectbox("Menu", menu)

# ------------------ USERS ------------------
if choice == "Users":
    st.header("Manage Users")

    st.subheader("Add User")
    username = st.text_input("Username")
    email = st.text_input("Email")
    if st.button("Add User"):
        payload = {"username": username, "email": email}
        res = requests.post(f"{BASE_URL}/users/", json=payload).json()
        st.success(res.get("Message"))

    st.subheader("All Users")
    res = requests.get(f"{BASE_URL}/users/").json()
    users = res.get("data", [])
    if users:
        for u in users:
            st.write(f"ID: {u['id']} | Username: {u['username']} | Email: {u['email']}")
            if st.button(f"Delete User {u['id']}", key=f"del_{u['id']}"):
                d = requests.delete(f"{BASE_URL}/users/{u['id']}").json()
                st.success(d.get("Message"))

# ------------------ FACTS ------------------
elif choice == "Facts":
    st.header("Manage Facts")

    st.subheader("Add Fact")
    content = st.text_input("Fact Content")
    category = st.text_input("Category")
    user_id = st.number_input("User ID (optional)", min_value=0, value=0)
    if st.button("Add Fact"):
        payload = {"content": content, "category": category, "user_id": user_id or None}
        res = requests.post(f"{BASE_URL}/facts/", json=payload).json()
        st.success(res.get("Message"))

    st.subheader("All Facts")
    res = requests.get(f"{BASE_URL}/facts/").json()
    facts = res.get("data", [])
    if facts:
        for f in facts:
            st.write(f"ID: {f['id']} | {f['content']} ({f['category']}) | User: {f.get('user_id')}")
            if st.button(f"Delete Fact {f['id']}", key=f"del_fact_{f['id']}"):
                d = requests.delete(f"{BASE_URL}/facts/{f['id']}").json()
                st.success(d.get("Message"))

# ------------------ RANDOM FACT ------------------
elif choice == "Random Fact":
    st.header("Get Random Fact")
    category = st.text_input("Category (optional)")
    if st.button("Get Random Fact"):
        params = {"category": category} if category else {}
        res = requests.get(f"{BASE_URL}/facts/random/", params=params).json()
        if res.get("Success"):
            fact = res.get("Fact")
            st.success(f"{fact['content']} ({fact['category']})")
        else:
            st.error(res.get("Message"))

# ------------------ FAVORITES ------------------
elif choice == "Favorites":
    st.header("Manage Favorites")

    st.subheader("Add Favorite")
    user_id = st.number_input("User ID", min_value=1)
    fact_id = st.number_input("Fact ID", min_value=1)
    if st.button("Add Favorite"):
        payload = {"user_id": user_id, "fact_id": fact_id}
        res = requests.post(f"{BASE_URL}/favorites/", json=payload).json()
        st.success(res.get("Message"))

    st.subheader("View User Favorites")
    user_id_fav = st.number_input("User ID for Favorites", min_value=1, key="fav_user_id")
    if st.button("Show Favorites"):
        res = requests.get(f"{BASE_URL}/favorites/{user_id_fav}").json()
        favorites = res.get("data", [])
        if favorites:
            for f in favorites:
                st.write(f"Favorite ID: {f['id']} | Fact ID: {f['fact_id']}")
                if st.button(f"Remove Favorite {f['id']}", key=f"del_fav_{f['id']}"):
                    d = requests.delete(f"{BASE_URL}/favorites/{f['id']}").json()
                    st.success(d.get("Message"))
        else:
            st.info("No favorites found for this user.")
