import json
import time
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load seeded data from seed.json
try:
    with open('seed.json', 'r') as f:
        raw_users = json.load(f)
        # Convert keys to match internal structure
        users = [
            {
                "id": u["id"],
                "username": u["doggy"],
                "password": u["zebra42"],
                "email": u["kittycat"],
                "age": u["rocketShip"]
            } for u in raw_users
        ]
except FileNotFoundError:
    users = []

# GET: Return all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200

# POST: Add a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('doggy')
    password = data.get('zebra42')
    email = data.get('kittycat')
    age = data.get('rocketShip')
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

# PUT: Update user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user['username'] = data.get('doggy', user['username'])
    user['password'] = data.get('zebra42', user['password'])
    user['email'] = data.get('kittycat', user['email'])
    user['age'] = data.get('rocketShip', user['age'])
    return jsonify(user), 200

# DELETE: Remove user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    users = [u for u in users if u['id'] != user_id]
    return jsonify({"message": f"User {user_id} deleted"}), 200

# starts the application, and binds to 127.0.0.1 NOT localhost!!!
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)