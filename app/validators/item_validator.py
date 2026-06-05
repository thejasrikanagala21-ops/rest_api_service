"""
Item Validator Module
Enforces strict schema and data type rules on incoming JSON requests.
Prevents malformed data from reaching the core business logic.
"""

class ItemValidator:
    @staticmethod
    def validate_item_payload(data: dict, is_update: bool = False) -> tuple[bool, dict | None]:
        """
        Validates the JSON payload for creating or updating an Item.
        Returns (is_valid, error_dictionary).
        """
        if not data or not isinstance(data, dict):
            return False, {"code": "BAD_REQUEST", "message": "Invalid or missing JSON payload."}

        name = data.get("name")
        description = data.get("description")

        # 1. Validate 'name' (Required for creation, optional for update but must be valid if provided)
        if not is_update or "name" in data:
            if not name or not isinstance(name, str) or len(name.strip()) < 3:
                return False, {
                    "code": "VALIDATION_ERROR", 
                    "message": "Field 'name' is required and must be a string of at least 3 characters."
                }
            if len(name) > 100:
                return False, {
                    "code": "VALIDATION_ERROR",
                    "message": "Field 'name' cannot exceed 100 characters."
                }

        # 2. Validate 'description' (Optional, but must be valid if provided)
        if "description" in data:
            if not isinstance(description, str):
                return False, {
                    "code": "VALIDATION_ERROR",
                    "message": "Field 'description' must be a string."
                }
            if len(description) > 500:
                return False, {
                    "code": "VALIDATION_ERROR",
                    "message": "Field 'description' cannot exceed 500 characters."
                }

        return True, None