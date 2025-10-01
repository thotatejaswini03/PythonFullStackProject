import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

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
                try:
                    res_data = res.json()
                except Exception:
                    st.error(f"Registration failed. Status: {res.status_code} Response: {res.text}")
                    return
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
                try:
                    res_data = res.json()
                except Exception:
                    st.error(f"Login failed. Status: {res.status_code} Response: {res.text}")
                    return
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
        st.query_params = {"page": ["home"]}
        st.stop()  


def show_discover():
    st.header(f"Discover Fun Facts - Welcome, {st.session_state.get('username','User')}!")
    # Get categories
    try:
        res = requests.get(f"{BASE_URL}/facts/")
        if res.status_code == 200:
            facts = res.json().get("data", [])
            categories = sorted(list(set([fact["category"] for fact in facts])))
        else:
            categories = []
            st.error(f"Failed to fetch categories. {res.text}")
    except Exception as e:
        st.error(f"Error fetching categories: {e}")
        categories = []

    if categories:
        selected_category = st.selectbox("Select a category", categories, key="disc_cat")
        if st.button("Generate Fun Fact", key="gen_fact_btn"):
            params = {"category": selected_category}
            try:
                resp = requests.get(f"{BASE_URL}/facts/random/", params=params)
                if resp.status_code == 200:
                    try:
                        resp_data = resp.json()
                    except Exception:
                        st.error(f"Error: Status {resp.status_code}, Response: {resp.text}")
                        return
                    if resp_data.get("Success"):
                        fact = resp_data["Fact"]
                        st.info(fact["fact_text"])
                    else:
                        st.warning(resp_data.get("Message", "No fun fact available for this category."))
                else:
                    st.error(f"Failed to fetch fun fact. Status: {resp.status_code} Response: {resp.text}")
            except Exception as e:
                st.error(f"Error fetching fun fact: {e}")
    else:
        st.warning("No categories found. Add some facts first.")

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
    menu = ["Discover Fun Facts", "Add Fun Fact"]  # Favorites removed
    if 'page' not in st.session_state or st.session_state['page'] not in menu:
        st.session_state['page'] = "Discover Fun Facts"
    page = st.sidebar.selectbox("Menu", menu, index=menu.index(st.session_state['page']))
    st.session_state['page'] = page

    if st.session_state['page'] == "Discover Fun Facts":
        show_discover()
    elif st.session_state['page'] == "Add Fun Fact":
        show_add_fact()
