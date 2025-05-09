import streamlit as st 
import hashlib
import json
import os
from cryptography.fernet import Fernet

# File paths

USER_FILE ="user..json"
DATA_FILE = "data.json"
KEY_FILE = "key.key"

# Function to load data from a file
if os.path.exists(KEY_FILE):
    with open(KEY_FILE, "rb") as f:
        KEY = f.read()
else:
    KEY = Fernet.generate_key()
    with open (KEY_FILE, "wb") as f:
        f.write(KEY)

cipher = Fernet(KEY)    

# Helpers
def hashing_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def encrypt_data_text(txt):
    return cipher.encrypt(txt.encode()).decode()

def decrypt_data_text(txt):
    return cipher.decrypt(txt.encode()).decode()

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

    
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


users = load_users()
data_storage = load_data()

# Session state defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

#  UI

st.title("🔐 SecureVault")

sidebar = st.sidebar.selectbox("Choose an option", ["🏠 Home", "📝 Register", "🔐 Sign In", "📥 Store Data", "📤 Retrieve Data"])

#Home
if sidebar == "🏠 Home":
    st.header("Welcome to SecureVault!")
    st.markdown("Easily encrypt and store your sensitive data using a secure passkey. Register and log in to begin.")

# register

elif sidebar == "📝 Register":
    st.header("📝 Register")
    new_user = st.text_input("Choose a username")
    new_password = st.text_input("Choose a password", type="password")
    if st.button("Register"):
        if new_user in users:
            st.warning("Username already exists!. Try signing in.")

        elif new_user and new_password:
            users[new_user] = hashing_password(new_password)
            save_users(users)
            st.success("User registered successfully!")
        else:
            st.error("Please fill in all fields.")

# Sign In
elif sidebar == "🔐 Sign In":
    st.header("🔐 Sign In")
    user = st.text_input("Enter your username")
    pw = st.text_input("Enter your password", type="password")
    if st.button("Login"):
        if user in users :
            if hashing_password(pw) == users[user]:
                st.session_state.logged_in = True
                st.session_state.username = user
                st.session_state.failed_attempts = 0
                st.success(f"Welcome back, {user}!")
            else:
                st.session_state.failed_attempts += 1
                reaming_attempts = 3 - st.session_state.failed_attempts
                if reaming_attempts > 0:
                    st.warning(f"Incorrect password. You have {reaming_attempts} attempts left.")
                else:
                    st.error("Too many failed attempts.Login Locked.")
        else:
            st.warning("Username not found. Please register.")    



# Store Data
elif sidebar == "📥 Store Data":
    if not st.session_state.logged_in:
        st.error("🔐 Please sign in to access this feature.")
    else:
        st.header("📥 Store Secret")
        key = st.text_input("Enter key name")
        secret = st.text_area("Your secret")
        passkey = st.text_input("Create a passkey", type="password")
        if st.button("Encrypt and Store"):
            if key and secret and passkey:
                uid = st.session_state.username
                encrypted = encrypt_data_text(secret)
                hasehed_passkey = hashing_password(passkey)
                if uid not in data_storage:
                    data_storage[uid] = {}
                data_storage[uid][key] = {"text": encrypted, "pass":hasehed_passkey}
                save_data(data_storage)
                st.success("Data stored successfully!")
            else:
                st.error("Please fill in all fields.")
            

# Retrieve Data 
elif sidebar == "📤 Retrieve Data":
    if not st.session_state.logged_in:
        st.error("🔐 Please sign in to access this feature.")
    elif st.session_state.failed_attempts >= 3:
        st.warning("🚫 Too many incorrect attempts. Please log in again.")
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()
    else: 
        st.header("📤 Retrieve Secret")
        key = st.text_input("Enter key name you stored")
        passkey = st.text_input("Enter your passkey", type="password")
        if st.button("Decrypt and Retrieve"):
            uid = st.session_state.username
            user_data = data_storage.get(uid, {})
            record = user_data.get(key)
            if record:
                if hashing_password(passkey) == record["pass"]:
                    decrypted = decrypt_data_text(record["text"])
                    st.success(f"✅ Decrypted data: {decrypted}")
                    st.session_state.failed_attempts = 0
                else:
                    st.session_state.failed_attempts += 1
                    left = 3 - st.session_state.failed_attempts
                    st.error(f"❌ Incorrect passkey. You have {left} attempts left.")
                    if st.session_state.failed_attempts >=3:
                        st.error("🚫 Too many incorrect attempts. Please log in again.")
                        st.session_state.logged_in = False
                        st.session_state.username = ""
                        st.experimental_rerun()
            else:
                st.warning("⚠️ Key not found.")
    