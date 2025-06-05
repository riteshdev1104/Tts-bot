from flask import Flask, request, render_template
import os

app = Flask(__name__)

ADMIN_PASSWORD = "0110409"
LOG_FILE = "logs/messages.log"

@app.route('/')
def home():
    return render_template("login.html")

@app.route('/admin', methods=["POST"])
def admin():
    password = request.form.get("password")
    if password == ADMIN_PASSWORD:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                log_lines = f.readlines()
        else:
            log_lines = ["No logs found."]
        return render_template("dashboard.html", logs=log_lines)
    else:
        return "Incorrect password", 403

@app.route('/log', methods=["POST"])
def log_message():
    msg = request.json.get("msg")
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    return "Logged", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
