from flask import Flask, request, render_template
import os

app = Flask(__name__)

ADMIN_PASSWORD = "0110409"
logs = []

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/admin', methods=["POST"])
def admin():
    password = request.form.get("password")
    if password == ADMIN_PASSWORD:
        return render_template("dashboard.html", logs=logs)
    else:
        return "Incorrect password", 403

@app.route('/log', methods=["POST"])
def log_message():
    msg = request.json.get("msg")
    logs.append(msg)
    return "Logged", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
