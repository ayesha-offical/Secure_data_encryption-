# 🔐 SecureVault - Streamlit Based Secure Data Storage App

**SecureVault** is a Streamlit-based secure storage system that allows users to **encrypt and retrieve secret text data** using a unique passkey.
It also includes a **user authentication system**, passkey protection, and a **3-attempt lockout mechanism**.

---

## 🚀 Features

* 🧑‍💻 User Registration & Login System
* 🔐 Secure encryption using `Fernet` from `cryptography`
* 🔑 Unique passkey protection per data entry
* ⟳ 3 Failed Attempts → Auto logout for security
* 📂 Data & user info saved in local JSON files
* ✨ Clean and user-friendly Streamlit UI

---

## 🧠 How It Works

1. **Register** as a new user (username + password)
2. **Login** to access storage features
3. **Store Data:** Enter a custom key, your secret message, and a passkey → app encrypts it
4. **Retrieve Data:** Provide key + passkey to securely decrypt the message
5. After **3 wrong passkey attempts**, user is **logged out automatically**

---

## 🧱 Tech Stack

* 🐍 Python 3
* 📆 Streamlit
* 🔐 Cryptography (Fernet)
* 🧠 JSON for local storage
* ⟳ hashlib for password hashing

---

## 📂 File Structure

```
📁 SecureVault/
🔍 main.py              # Main Streamlit app
🔍 users.json           # Stores registered users
🔍 user_data.json       # Stores encrypted data
🔍 fernet_key.key       # Encryption key (generated automatically)
```

---

## 💡 OOP Concepts Used

| Concept        | Where it's used                               |
| -------------- | --------------------------------------------- |
| Encapsulation  | Hashing passwords, encryption inside helpers  |
| Abstraction    | Functions hide logic of encryption/decryption |
| State Handling | Session-based login management                |

---

## 🔧 How to Run

```bash
pip install streamlit cryptography
streamlit run main.py
```

---

## 🔍 Test It Online

Want to test it without setup?
🌐 [Try it on Streamlit Cloud](https://ma5jbenml4954mgtcpo5ra.streamlit.app/) 

---

## ✨ Author

Made with ❤️ by Ayesha
Need help? Ping me anytime.
