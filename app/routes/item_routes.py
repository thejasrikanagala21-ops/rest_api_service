"""
Item Resource Routes Module
Presentation layer for managing 'Item' resources (Create, Read, Update, Delete).
Enforces JWT authentication for protected operations and delegates to ItemService.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

# The ItemService will be implemented in Phase 3
from app.services.item_service import ItemService

item_bp = Blueprint('items', __name__)
item_service = ItemService()

@item_bp.route('', methods=['GET'])
def get_items():
    """
    Retrieves a list of all items. 
    Public endpoint (no JWT required).
    """
    result, status_code = item_service.get_all_items()
    return jsonify(result), status_code

@item_bp.route('/<string:item_id>', methods=['GET'])
def get_item(item_id):
    """
    Retrieves a specific item by its ID.
    Public endpoint.
    """
    result, status_code = item_service.get_item_by_id(item_id)
    return jsonify(result), status_code

@item_bp.route('', methods=['POST'])
@jwt_required()
def create_item():
    """
    Creates a new item.
    Protected endpoint (requires valid JWT access token).
    Expected JSON: { "name": "...", "description": "..." }
    """
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False, 
            "error": {"code": "BAD_REQUEST", "message": "Missing JSON payload"}
        }), 400
        
    result, status_code = item_service.create_item(data)
    return jsonify(result), status_code

@item_bp.route('/<string:item_id>', methods=['PUT'])
@jwt_required()
def update_item(item_id):
    """
    Updates an existing item completely.
    Protected endpoint.
    Expected JSON: { "name": "...", "description": "..." }
    """
    data = request.get_json()
    if not data:
        return jsonify({
            "success": False, 
            "error": {"code": "BAD_REQUEST", "message": "Missing JSON payload"}
        }), 400
        
    result, status_code = item_service.update_item(item_id, data)
    return jsonify(result), status_code

@item_bp.route('/<string:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    """
    Deletes an item from the system.
    Protected endpoint.
    """
    result, status_code = item_service.delete_item(item_id)
    return jsonify(result), status_code