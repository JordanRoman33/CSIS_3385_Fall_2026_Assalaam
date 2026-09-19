import json
import time
from pathlib import Path
from flask import Flask, jsonify, request

app = Flask(__name__)
DATA_FILE = Path(__file__).with_name("seed.json")

PAGE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>Create User</title>
  <style>
    body { background:#111; font-family:Segoe UI,sans-serif; }
    .card { width:360px; margin:40px auto; background:#2b2b2b; color:#fff;
            padding:28px; border-radius:10px; }
    h1 { margin:0 0 20px; }
    label { display:block; margin:14px 0 8px; }
    input { width:100%; height:40px; border:0; border-radius:8px;
            background:#3a3a3a; color:#fff; padding:0 12px; box-sizing:border-box; }
    button { width:100%; height:44px; margin-top:22px; border:0; border-radius:8px;
             background:#5eb8f7; color:#fff; font-size:16px; cursor:pointer; }
    .msg { margin-top:12px; }
  </style>
</head>
<body>
  <form class="card" id="form">
    <h1>Create User</h1>
    <label>Username:</label><input id="username" required />
    <label>Password:</label><input id="password" type="password" required />
    <label>Age:</label><input id="age" type="number" required />
    <label>Email:</label><input id="email" type="email" required />
    <div class="msg" id="msg"></div>
    <button type="submit">Submit</button>
  </form>
  <script>
    document.getElementById("form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const msg = document.getElementById("msg");
      const res = await fetch("/users", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          doggy: document.getElementById("username").value,
          zebra42: document.getElementById("password").value,
          rocketShip: Number(document.getElementById("age").value),
          kittycat: document.getElementById("email").value
        })
      });
      const data = await res.json();
      msg.textContent = res.ok ? "User created: " + (data.username || "ok") : (data.error || "Error");
    });
  </script>
</body>
</html>
"""

def load_users():
    try:
        with DATA_FILE.open() as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except FileNotFoundError:
        return []

def save_users(data):
    with DATA_FILE.open("w") as f:
        json.dump(data, f, indent=2)

users = load_users()

@app.get("/")
def home():
    return PAGE

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("doggy")
    password = data.get("zebra42")
    email = data.get("kittycat")
    age = data.get("rocketShip")
    timestamp = str(int(time.time()))[-6:]
    new_user = {
        "id": int(f"{len(users)}{timestamp}"),
        "username": username,
        "password": password,
        "email": email,
        "age": age
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user["username"] = data.get("doggy", user["username"])
    user["password"] = data.get("zebra42", user["password"])
    user["email"] = data.get("kittycat", user["email"])
    user["age"] = data.get("rocketShip", user["age"])
    return jsonify(user), 200

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    users = [u for u in users if u.get("id") != user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    if not DATA_FILE.exists():
        save_users([])
    app.run(host="0.0.0.0", port=5000, debug=True)