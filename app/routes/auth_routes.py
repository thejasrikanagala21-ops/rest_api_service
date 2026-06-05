"""
Authentication Routes Module
Presentation layer for user registration, login, and token refresh.
Strictly handles HTTP semantics and delegates business logic to AuthService.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

# The AuthService will be implemented in Phase 3
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user in the system.
    Expected JSON: { "username": "...", "password": "..." }
    """
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False, 
            "error": {"code": "BAD_REQUEST", "message": "Missing JSON payload"}
        }), 400
        
    result, status_code = auth_service.register_user(data)
    return jsonify(result), status_code

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticates a user and issues JWT access and refresh tokens.
    Expected JSON: { "username": "...", "password": "..." }
    """
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False, 
            "error": {"code": "BAD_REQUEST", "message": "Missing JSON payload"}
        }), 400
        
    result, status_code = auth_service.login_user(data)
    return jsonify(result), status_code

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Issues a new access token using a valid refresh token.
    Requires header -> Authorization: Bearer <refresh_token>
    """
    current_user = get_jwt_identity()
    result, status_code = auth_service.refresh_access_token(current_user)
    return jsonify(result), status_code