from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)

# 🔒 Secure session configuration
app.secret_key = "super_secure_secret_key"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
Session(app)

# Dummy user database
users = {"admin": "password123"}

# Store incoming data (For testing; use a database in real projects)
sms_data_store = []
sim_data_store = []

# 🟢 Login Page
@app.route('/')
def login_page():
    if "user" in session:
        return redirect(url_for("dashboard_page"))  
    return render_template('login.html')

# 🟢 Dashboard Page
@app.route('/dashboard')
def dashboard_page():
    if "user" not in session:
        return redirect(url_for("login_page"))  
    return render_template('dashboard.html', sms_data=sms_data_store, sim_data=sim_data_store)

# 🟢 Login API
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")  
    password = request.form.get("password")

    if users.get(username) == password:
        session["user"] = username
        return redirect(url_for("dashboard_page"))  
    else:
        return "Invalid credentials", 401

# 🟢 Logout API
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login_page"))

# 🟢 API to Receive SMS Data
@app.route('/api/sms', methods=['POST'])
def receive_sms():
    data = request.json
    print("Received SMS Data:", data)

    sms_data_store.append(data)  # Store in memory (use DB in real projects)
    return jsonify({"message": "SMS received successfully!"}), 200

# 🟢 API to Receive SIM Details
@app.route('/api/sim', methods=['POST'])
def receive_sim():
    data = request.json
    print("Received SIM Data:", data)

    sim_data_store.append(data)  # Store in memory (use DB in real projects)
    return jsonify({"message": "SIM details received successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
