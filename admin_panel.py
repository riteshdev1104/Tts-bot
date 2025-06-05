from flask import Flask, request, render_template
import os
from dotenv import load_dotenv

load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

app = Flask(__name__)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            with open("logs/messages.log", "r") as f:
                logs = f.read()
            return render_template("admin.html", logs=logs)
        else:
            return "Incorrect Password", 403
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
