"""
Item Service Module
Handles business logic for the Item resource.
Acts as the intermediary between the presentation layer (routes) and the data layer (repository).
"""
# The ItemRepository will be implemented in Phase 4
from app.repositories.item_repository import ItemRepository

class ItemService:
    def __init__(self):
        self.repository = ItemRepository()

    def get_all_items(self) -> tuple[dict, int]:
        """
        Retrieves all items from the repository.
        """
        items = self.repository.find_all()
        return {"success": True, "data": items}, 200

    def get_item_by_id(self, item_id: str) -> tuple[dict, int]:
        """
        Retrieves a single item. Returns a 404 structured error if missing.
        """
        item = self.repository.find_by_id(item_id)
        if not item:
            return {
                "success": False, 
                "error": {"code": "RESOURCE_NOT_FOUND", "message": f"Item with ID '{item_id}' not found."}
            }, 404
            
        return {"success": True, "data": item}, 200

    def create_item(self, data: dict) -> tuple[dict, int]:
        """
        Creates a new item. Enforces basic business validation before saving.
        """
        name = data.get("name")
        
        # Basic business rule: Items must have a name
        if not name or str(name).strip() == "":
            return {
                "success": False, 
                "error": {"code": "VALIDATION_ERROR", "message": "Item 'name' is required and cannot be empty."}
            }, 400

        new_item = self.repository.create(data)
        return {"success": True, "data": new_item}, 201

    def update_item(self, item_id: str, data: dict) -> tuple[dict, int]:
        """
        Updates an existing item. Returns 404 if the item doesn't exist.
        """
        updated_item = self.repository.update(item_id, data)
        if not updated_item:
            return {
                "success": False, 
                "error": {"code": "RESOURCE_NOT_FOUND", "message": f"Cannot update. Item with ID '{item_id}' not found."}
            }, 404
            
        return {"success": True, "data": updated_item}, 200

    def delete_item(self, item_id: str) -> tuple[dict, int]:
        """
        Deletes an item. Returns 404 if the item doesn't exist.
        """
        deleted = self.repository.delete(item_id)
        if not deleted:
            return {
                "success": False, 
                "error": {"code": "RESOURCE_NOT_FOUND", "message": f"Cannot delete. Item with ID '{item_id}' not found."}
            }, 404
            
        return {"success": True, "message": "Item deleted successfully"}, 200