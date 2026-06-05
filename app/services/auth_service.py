"""
Authentication Service Module
Handles business logic for user registration, authentication, and JWT token issuance.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthService:
    def __init__(self):
        # In a real system, this would inject a UserRepository.
        # For demonstration, we use a simple in-memory store.
        self.users_db = {} 

    def register_user(self, data: dict) -> tuple[dict, int]:
        """
        Registers a new user after verifying the username is unique.
        Returns a tuple of (Response Data, HTTP Status Code).
        """
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"success": False, "error": {"code": "VALIDATION_ERROR", "message": "Username and password required"}}, 400

        if username in self.users_db:
            return {"success": False, "error": {"code": "CONFLICT", "message": "Username already exists"}}, 409

        # Store user with hashed password (NEVER store plaintext)
        self.users_db[username] = {
            "username": username,
            "password_hash": generate_password_hash(password)
        }

        return {"success": True, "message": "User registered successfully"}, 201

    def login_user(self, data: dict) -> tuple[dict, int]:
        """
        Verifies credentials and issues JWT access and refresh tokens.
        """
        username = data.get("username")
        password = data.get("password")

        user = self.users_db.get(username)

        # Constant-time comparison using check_password_hash to prevent timing attacks
        if not user or not check_password_hash(user["password_hash"], password):
            return {"success": False, "error": {"code": "UNAUTHORIZED", "message": "Invalid username or password"}}, 401

        # Generate tokens
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return {
            "success": True,
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"
            }
        }, 200

    def refresh_access_token(self, username: str) -> tuple[dict, int]:
        """
        Issues a new access token for a valid refresh token.
        """
        # Ensure user still exists/is active in the system
        if username not in self.users_db:
            return {"success": False, "error": {"code": "UNAUTHORIZED", "message": "User account no longer valid"}}, 401
            
        new_access_token = create_access_token(identity=username)
        
        return {
            "success": True,
            "data": {
                "access_token": new_access_token,
                "token_type": "Bearer"
            }
        }, 200