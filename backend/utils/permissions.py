from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User

def role_required(*allowed_roles):
    """
    Decorator to restrict access to specific roles.
    Usage: @role_required('Administrator', 'Dispatcher')
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # 1. Verify the token is valid and present
            verify_jwt_in_request()
            
            # 2. Get user ID from the token
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            # 3. Check if user exists and is active
            if not user or not user.is_active:
                return jsonify({"success": False, "message": "User not found or deactivated"}), 403
                
            # 4. Check if user has the required role
            if user.role not in allowed_roles:
                return jsonify({
                    "success": False, 
                    "message": f"Access denied. Requires one of roles: {', '.join(allowed_roles)}"
                }), 403
                
            # 5. If all checks pass, execute the original route function
            return fn(*args, **kwargs)
        return wrapper
    return decorator