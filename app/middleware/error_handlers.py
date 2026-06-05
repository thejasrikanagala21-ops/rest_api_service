"""
Global Error Handling Middleware
Intercepts Flask framework exceptions (404, 405, 500) and JWT authentication errors,
standardizing them into a consistent JSON response format for the API consumer.
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging

logger = logging.getLogger("ErrorHandlers")

def register_error_handlers(app):
    """
    Registers global error interceptors on the Flask application instance.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": {
                "code": "BAD_REQUEST",
                "message": "The server could not understand the request due to invalid syntax."
            }
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": {
                "code": "UNAUTHORIZED",
                "message": "Authentication is required and has failed or has not yet been provided."
            }
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": {
                "code": "FORBIDDEN",
                "message": "The client does not have access rights to the content."
            }
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "The requested resource could not be found on this server."
            }
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": {
                "code": "METHOD_NOT_ALLOWED",
                "message": "The method specified in the request is not allowed for the resource identified by the request URI."
            }
        }), 405

    @app.errorhandler(Exception)
    def handle_exception(e):
        """
        Fallback for all unhandled server exceptions (500).
        Prevents HTML stack traces from leaking to the client.
        """
        # Pass through HTTP errors that we haven't explicitly caught above
        if isinstance(e, HTTPException):
            return jsonify({
                "success": False,
                "error": {
                    "code": e.name.upper().replace(" ", "_"),
                    "message": e.description
                }
            }), e.code

        # Log the actual exception for internal debugging, but obscure it from the client
        logger.error(f"Unhandled Internal Server Error: {str(e)}", exc_info=True)
        
        return jsonify({
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred while processing your request."
            }
        }), 500