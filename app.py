from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)

# 🔴 Secure session configuration
app.secret_key = "super_secure_secret_key"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True

Session(app)

# Dummy user database
users = {"admin": "password123"}

# 🔴 Storage for user data (replace with DB in real apps)
user_data = {}

@app.route('/')
def login_page():
    if "user" in session:
        return redirect(url_for("dashboard_page"))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    if "user" not in session:
        return redirect(url_for("login_page"))
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")  # 🔴 Fix: Use request.form instead of JSON
    password = request.form.get("password")

    if users.get(username) == password:
        session["user"] = username
        return redirect(url_for("dashboard_page"))  # 🔴 Fix: Redirect properly
    else:
        return "Invalid credentials", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login_page"))

@app.route('/update_user_data', methods=['POST'])
def update_user_data():
    data = request.json
    print("Received Data:", data)  # Debugging

    # 🔴 Store data (Simulated database)
    user_data["user1"] = data

    return jsonify({"message": "Data received successfully!"})

# 🔴 Run the Flask app on all network interfaces (public access)
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
