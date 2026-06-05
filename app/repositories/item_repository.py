"""
Item Repository Module
Data access layer abstraction for the 'Item' resource.
Simulates a database using an in-memory data store for demonstration.
"""
import uuid
from datetime import datetime, timezone

class ItemRepository:
    def __init__(self):
        # In a real-world scenario, this would be a DB connection pool (e.g., SQLAlchemy)
        # We use a class-level dictionary to persist state across requests for this demo.
        if not hasattr(self.__class__, '_db'):
            self.__class__._db = {}

    @property
    def db(self):
        return self.__class__._db

    def find_all(self) -> list:
        """Retrieves all items from the database."""
        return list(self.db.values())

    def find_by_id(self, item_id: str) -> dict | None:
        """Retrieves an item by its unique ID."""
        return self.db.get(item_id)

    def create(self, data: dict) -> dict:
        """Creates a new item and persists it to the database."""
        item_id = str(uuid.uuid4())
        
        new_item = {
            "id": item_id,
            "name": data.get("name"),
            "description": data.get("description", ""),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        
        self.db[item_id] = new_item
        return new_item

    def update(self, item_id: str, data: dict) -> dict | None:
        """Updates an existing item completely."""
        if item_id not in self.db:
            return None
            
        # Retain original ID and creation date, update the rest
        updated_item = self.db[item_id]
        updated_item["name"] = data.get("name", updated_item["name"])
        updated_item["description"] = data.get("description", updated_item["description"])
        
        self.db[item_id] = updated_item
        return updated_item

    def delete(self, item_id: str) -> bool:
        """Deletes an item from the database. Returns True if successful."""
        if item_id in self.db:
            del self.db[item_id]
            return True
        return False