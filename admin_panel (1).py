
from flask import Flask, request, render_template_string
import os
import json

app = Flask(__name__)

# Change this password to your secure one
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "tagarA11")

DATA_FILE = "users.json"

@app.route("/")
def index():
    password = request.args.get("password")
    if password != ADMIN_PASSWORD:
        return "Unauthorized", 403

    if not os.path.exists(DATA_FILE):
        return "No user data found."

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    users_list = ""
    for user_id, info in data.items():
        users_list += f"<li><strong>ID:</strong> {user_id}, <strong>Email:</strong> {info.get('email')}</li>"

    html = f"""
    <h2>Registered Users:</h2>
    <ul>{users_list}</ul>
    """
    return render_template_string(html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
