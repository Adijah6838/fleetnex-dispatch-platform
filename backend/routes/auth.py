from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"success": False, "message": "Username already exists"}), 409
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"success": False, "message": "Email already exists"}), 409

    # Default to Viewer if role is not provided
    role = data.get('role', 'Viewer')
    if role not in ['Administrator', 'Dispatcher', 'Fleet Manager', 'Viewer']:
        return jsonify({"success": False, "message": "Invalid role"}), 400

    user = User(username=data['username'], email=data['email'], role=role)
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "data": {"id": user.id, "username": user.username, "role": user.role}
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"success": False, "message": "Missing username or password"}), 400

    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"success": False, "message": "Invalid credentials"}), 401
        
    if not user.is_active:
        return jsonify({"success": False, "message": "Account is deactivated"}), 403

    # Create the JWT token
    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "user": {"id": user.id, "username": user.username, "role": user.role}
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
        
    return jsonify({
        "success": True,
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({"success": True, "message": "Successfully logged out"}), 200