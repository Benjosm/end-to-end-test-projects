import jwt
import logging
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, current_app, g
from sqlalchemy.exc import IntegrityError
from email_validator import validate_email, EmailNotValidError
from inventory_management.models.user import User, Role
from inventory_management.utils.database import get_db
from inventory_management.utils.validators import validate_password

auth_bp = Blueprint("auth", __name__)
logger = logging.getLogger(__name__)

def generate_token(user_id):
    """Generate a JWT token for the user."""
    expiration = datetime.utcnow() + current_app.config["JWT_EXPIRATION"]
    payload = {
        "user_id": user_id,
        "exp": expiration
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ["username", "email", "password", "role_id"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    # Validate email format
    try:
        validate_email(data["email"])
    except EmailNotValidError as e:
        return jsonify({"error": str(e)}), 400
    
    # Validate password strength
    password_validation = validate_password(data["password"])
    if not password_validation["valid"]:
        return jsonify({"error": password_validation["message"]}), 400
    
    # Create new user
    user = User(
        username=data["username"],
        email=data["email"],
        role_id=data["role_id"],
        first_name=data.get("first_name", ""),
        last_name=data.get("last_name", "")
    )
    user.set_password(data["password"])
    
    # Add to database
    db = get_db()
    try:
        db.add(user)
        db.commit()
    except IntegrityError:
        db.rollback()
        logger.warning(f"Registration failed: Username or email already exists - {data['username']}")
        return jsonify({"error": "Username or email already exists"}), 409
    
    logger.info(f"User registered: {user.username}")
    return jsonify({"message": "User registered successfully", "user_id": user.id}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate user and return JWT token."""
    data = request.get_json()
    
    # Validate required fields
    if "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400
    
    # Get user from database
    db = get_db()
    user = db.query(User).filter_by(username=data["username"]).first()
    
    # Check if user exists and password is correct
    if user is None or not user.check_password(data["password"]):
        logger.warning(f"Login failed: Invalid username or password - {data['username']}")
        return jsonify({"error": "Invalid username or password"}), 401
    
    # Check if user is active
    if not user.active:
        logger.warning(f"Login failed: Account is inactive - {data['username']}")
        return jsonify({"error": "Account is inactive"}), 403
    
    # Update last login timestamp
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Generate token
    token = generate_token(user.id)
    
    logger.info(f"User logged in: {user.username}")
    return jsonify({"token": token, "user_id": user.id}), 200

def verify_token(token):
    """Verify JWT token and return user ID."""
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return None

def auth_required(view_func):
    """Decorator for views that require authentication."""
    def wrapped_view(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header is missing or invalid"}), 401
        
        token = auth_header.split(" ")[1]
        user_id = verify_token(token)
        
        if user_id is None or user_id is False:
            return jsonify({"error": "Invalid or expired token"}), 401
        
        # Get user from database
        db = get_db()
        user = db.query(User).filter_by(id=user_id).first()
        
        if user is None or not user.active:
            return jsonify({"error": "User not found or inactive"}), 401
        
        # Store user in g for view functions to access
        g.user = user
        
        return view_func(*args, **kwargs)
    
    return wrapped_view

@auth_bp.route("/me", methods=["GET"])
@auth_required
def get_current_user():
    """Get the current authenticated user."""
    user = g.user
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role.name,
        "last_login": user.last_login.isoformat() if user.last_login else None,
    }), 200
