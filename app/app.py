"""
Core Application Factory Module
Initializes the Flask application instance, configures JWT lifecycle management,
and registers modular presentation blueprints alongside global error-handling middleware.
"""
import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from app.middleware.error_handlers import register_error_handlers
from app.routes.auth_routes import auth_bp
from app.routes.item_routes import item_bp

def create_app(config_overrides: dict = None) -> Flask:
    """
    Application factory pattern to instantiate and configure the Flask API service.
    """
    app = Flask(__name__)

    # Production Configuration Setups
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "prod-level-session-fallback-key-9x2c")
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "secure-jwt-architecture-token-8b1a")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 900
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 86400

    if config_overrides:
        app.config.update(config_overrides)

    # Initialize Extensible Security Layers
    jwt = JWTManager(app)

    # --- NEW: Intercept JWT-specific errors to maintain our standard JSON contract ---
    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return jsonify({
            "success": False,
            "error": {"code": "UNAUTHORIZED", "message": "Authentication token is missing."}
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify({
            "success": False,
            "error": {"code": "UNAUTHORIZED", "message": "The provided token is invalid."}
        }), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "success": False,
            "error": {"code": "UNAUTHORIZED", "message": "The token has expired."}
        }), 401
    # ---------------------------------------------------------------------------------

    # Register Global Middleware and Custom JSON Exception Interceptors
    register_error_handlers(app)

    # Attach Layered API Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(item_bp, url_prefix="/items")

    @app.route("/health", methods=["GET"])
    def health_check():
        """Liveness probe for infrastructure health checking."""
        return {"success": True, "status": "healthy"}, 200

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)