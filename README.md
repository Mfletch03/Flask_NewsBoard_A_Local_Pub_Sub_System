# 📰 CSE2102 Lab 5 — Pub/Sub Web App

This project was originally based on a **CSE2102 lab assignment** designed to create a **Publisher–Subscriber (Pub/Sub) model**.  

I expanded upon the lab to turn it into a more complete and practical project — a **local, Flask-based web application** that acts as a **news board**. Users can sign up to receive updates, while an admin can post announcements for all subscribers to see.

---

## 💡 Features

### 👤 User Features
- **Sign Up / Log In** – Users can create an account and log in securely.  
- **View Messages** – See the latest announcements posted by the admin.  
- **Change Password** – Users can update their password anytime.  
- **Unsubscribe** – Option to delete their account and stop receiving updates.

### 🛠️ Admin Dashboard
- **Post Messages** – Send announcements to all subscribers.  
- **View Subscribers** – See a list of all registered users.  
- **Remove Subscribers** – Option to delete user accounts.  
- **Change Admin Credentials** – Update admin username or password.  

---

## ⚙️ How to Run

1. **Download or clone the repository** into your GitHub Codespace or local environment.  
2. Make sure you have **Python** and **Flask** installed:  
   pip install flask
3. run this command:
    python3 flaskHttpServer.py
4. Once it’s running, open this URL in your browser:
    👉 http://127.0.0.1:5000
    (CTRL + click on Windows or CMD + click on Mac)

## 🔑 Test Accounts

- You can use these pre-made accounts to explore the app:
    **User Account**:
        - Username: test
        - Password: 1234

    **Admin Account**:
        - Username: admin
        - Password: password