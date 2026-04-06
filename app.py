# ============================================================
#  app.py — Flask app with PostgreSQL connection
#  Tests: health check, DB connectivity, basic CRUD
# ============================================================

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Import models after db is initialised (avoids circular imports)
from models import User

# ------------------------------------------------------------
# Health check — ALB hits this to confirm container is alive
# Must return 200 or ALB marks the task as unhealthy
# ------------------------------------------------------------
@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

# ------------------------------------------------------------
# DB check — verifies Flask can actually reach RDS
# ------------------------------------------------------------
@app.route("/db-check")
def db_check():
    try:
        db.session.execute(db.text("SELECT 1"))
        return jsonify({"database": "connected"}), 200
    except Exception as e:
        return jsonify({"database": "unreachable", "error": str(e)}), 500

# ------------------------------------------------------------
# Create a user  POST /users  { "name": "Alice", "email": "..." }
# ------------------------------------------------------------
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "name and email are required"}), 400

    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 201

# ------------------------------------------------------------
# List all users  GET /users
# ------------------------------------------------------------
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "name": u.name, "email": u.email}
        for u in users
    ]), 200

# ------------------------------------------------------------
# Root route
# ------------------------------------------------------------
@app.route("/")
def index():
    return jsonify({
        "message": "Flask app running on ECS",
        "routes": ["/health", "/db-check", "/users"]
    }), 200

# ------------------------------------------------------------
# Entry point — binds to 0.0.0.0 so ALB can reach the container
# ------------------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # creates tables if they don't exist
    app.run(host="0.0.0.0", port=5000, debug=False)
