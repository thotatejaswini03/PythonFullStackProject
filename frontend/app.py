import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

# ----------------- Pages -----------------
def show_home():
    st.title("🎉 Welcome to Fun Facts Generator!")
    st.write("Discover, share, and save amazing facts from around the world.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Register"):
            st.session_state['page'] = "Register"
    with col2:
        if st.button("Login"):
            st.session_state['page'] = "Login"

def show_register():
    st.header("Register a new account")
    username = st.text_input("Username", key="reg_username")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")
    if st.button("Register", key="register_btn"):
        if not username or not email or not password:
            st.error("All fields are required!")
        else:
            payload = {"username": username, "email": email, "password": password}
            try:
                res = requests.post(f"{BASE_URL}/auth/register/", json=payload)
                res_data = res.json()
                if res_data.get("Success"):
                    st.success(res_data.get("Message", "Account registered successfully! Please log in."))
                    st.session_state['page'] = "Login"
                else:
                    st.error(res_data.get("Message", "Registration failed"))
            except Exception as e:
                st.error(f"Error during registration: {e}")
    if st.button("Back to Home", key="reg_back"):
        st.session_state['page'] = "Home"

def show_login():
    st.header("Login to your account")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_btn"):
        if not email or not password:
            st.error("Email and password are required!")
        else:
            payload = {"email": email, "password": password}
            try:
                res = requests.post(f"{BASE_URL}/auth/login/", json=payload)
                res_data = res.json()
                if res_data.get("Success"):
                    st.session_state["user_id"] = res_data.get("user_id")
                    st.session_state["username"] = res_data.get("Message", "User")
                    st.session_state['page'] = "Discover Fun Facts"
                    st.success("Login successful! Welcome.")
                else:
                    st.error(res_data.get("Message", "Login failed"))
            except Exception as e:
                st.error(f"Error during login: {e}")
    if st.button("Back to Home", key="login_back"):
        st.session_state['page'] = "Home"

def show_logout():
    st.sidebar.markdown(f"👤 Logged in as: {st.session_state.get('username','User')}")
    if st.sidebar.button("Logout"):
        st.session_state.clear()  
        st.session_state['page'] = "Home"  
        st.stop()  

# ----------------- Discover Facts -----------------
def show_discover():
    st.header(f"Discover Fun Facts - Welcome, {st.session_state.get('username','User')}!")
    user_id = st.session_state.get("user_id")
    try:
        res = requests.get(f"{BASE_URL}/facts/")
        facts = res.json().get("data", [])
    except Exception as e:
        st.error(f"Error fetching facts: {e}")
        facts = []

    categories = sorted(list(set([fact["category"] for fact in facts]))) if facts else []
    if categories:
        selected_category = st.selectbox("Select a category", categories, key="disc_cat")
        filtered_facts = [f for f in facts if f["category"] == selected_category]
        for fact in filtered_facts:
            st.write(fact["fact_text"])
            if st.button("Add to Favorites", key=f"fav_{fact['id']}"):
                payload = {"user_id": user_id, "fact_id": fact["id"]}
                try:
                    res = requests.post(f"{BASE_URL}/favorites/add/", json=payload)
                    res_data = res.json()
                    if res_data.get("Success"):
                        st.success(res_data.get("Message", "Added to favorites!"))
                    else:
                        st.error(res_data.get("Message", "Failed to add to favorites"))
                except Exception as e:
                    st.error(f"Error adding to favorites: {e}")
    else:
        st.warning("No categories found. Add some facts first.")

# ----------------- Add Fun Fact -----------------
def show_add_fact():
    st.header("Share a New Fun Fact")
    category = st.text_input("Category", key="addf_cat")
    fact_text = st.text_area("Fun Fact", key="addf_text")
    if st.button("Add Fun Fact", key="addf_btn"):
        if not category or not fact_text:
            st.error("Category and fact text cannot be empty!")
        else:
            payload = {
                "content": fact_text,
                "category": category,
                "user_id": st.session_state.get("user_id")
            }
            try:
                res = requests.post(f"{BASE_URL}/facts/", json=payload)
                if res.status_code == 200:
                    st.success("Fun fact added!")
                else:
                    st.error(f"Unable to add fun fact. Status code: {res.status_code}, Response: {res.text}")
            except Exception as e:
                st.error(f"Error adding fun fact: {e}")

# ----------------- Favorites -----------------
def show_favorites():
    st.header("⭐ My Favorite Fun Facts")
    user_id = st.session_state.get("user_id")
    try:
        res = requests.get(f"{BASE_URL}/favorites/{user_id}")
        fav_data = res.json()
        favorites = fav_data.get("favorites", [])
        if not favorites:
            st.info("You have no favorite facts yet.")
        else:
            for fact in favorites:
                st.write(f"- ({fact['category']}) {fact['fact_text']}")
    except Exception as e:
        st.error(f"Error fetching favorites: {e}")

# ----------------- Main -----------------
if 'page' not in st.session_state:
    st.session_state['page'] = "Home"

if 'user_id' not in st.session_state:
    if st.session_state['page'] == "Register":
        show_register()
    elif st.session_state['page'] == "Login":
        show_login()
    else:
        show_home()
else:
    show_logout()
    menu = ["Discover Fun Facts", "Add Fun Fact", "My Favorites"]
    if 'page' not in st.session_state or st.session_state['page'] not in menu:
        st.session_state['page'] = "Discover Fun Facts"

    page = st.sidebar.selectbox("Menu", menu, index=menu.index(st.session_state['page']))
    st.session_state['page'] = page

    if st.session_state['page'] == "Discover Fun Facts":
        show_discover()
    elif st.session_state['page'] == "Add Fun Fact":
        show_add_fact()
    elif st.session_state['page'] == "My Favorites":
        show_favorites()
