"""In-memory storage for PromptLab

This module provides simple in-memory storage for prompts and collections.
In a production environment, this would be replaced with a database.
"""

from typing import Dict, List, Optional
from app.models import Prompt, Collection


class Storage:
    """In-memory persistence layer for prompts and collections.

    Attributes:
        _prompts (Dict[str, Prompt]): Stored prompt records keyed by ID.
        _collections (Dict[str, Collection]): Stored collections keyed by ID.
    """

    def __init__(self):
        self._prompts: Dict[str, Prompt] = {}
        self._collections: Dict[str, Collection] = {}
    
    # ============== Prompt Operations ==============
    
    def create_prompt(self, prompt: Prompt) -> Prompt:
        """Persist a prompt record.

        Args:
            prompt (Prompt): Prompt to store.

        Returns:
            Prompt: The stored prompt object.
        """
        self._prompts[prompt.id] = prompt
        return prompt
    
    def get_prompt(self, prompt_id: str) -> Optional[Prompt]:
        """Retrieve a prompt by ID.

        Args:
            prompt_id (str): Prompt identifier.

        Returns:
            Optional[Prompt]: Prompt if found, otherwise None.
        """
        return self._prompts.get(prompt_id)
    
    def get_all_prompts(self) -> List[Prompt]:
        """Return all prompts in the store.

        Returns:
            List[Prompt]: All resident prompts.
        """
        return list(self._prompts.values())
    
    def update_prompt(self, prompt_id: str, prompt: Prompt) -> Optional[Prompt]:
        """Replace an existing prompt with new data.

        Args:
            prompt_id (str): Identifier of the prompt to update.
            prompt (Prompt): Updated prompt payload.

        Returns:
            Optional[Prompt]: Updated prompt if it existed, otherwise None.
        """
        if prompt_id not in self._prompts:
            return None
        self._prompts[prompt_id] = prompt
        return prompt
    
    def delete_prompt(self, prompt_id: str) -> bool:
        """Remove a prompt from storage.

        Args:
            prompt_id (str): Identifier of the prompt to delete.

        Returns:
            bool: True if deletion occurred, False otherwise.
        """
        if prompt_id in self._prompts:
            del self._prompts[prompt_id]
            return True
        return False
    
    # ============== Collection Operations ==============
    
    def create_collection(self, collection: Collection) -> Collection:
        """Persist a collection record.

        Args:
            collection (Collection): Collection to store.

        Returns:
            Collection: The stored collection object.
        """
        self._collections[collection.id] = collection
        return collection
    
    def get_collection(self, collection_id: str) -> Optional[Collection]:
        """Fetch a collection by its identifier.

        Args:
            collection_id (str): Identifier of the collection.

        Returns:
            Optional[Collection]: The collection if present, otherwise None.
        """
        return self._collections.get(collection_id)
    
    def get_all_collections(self) -> List[Collection]:
        """Return every collection in storage.

        Returns:
            List[Collection]: All stored collections.
        """
        return list(self._collections.values())
    
    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection record.

        Args:
            collection_id (str): Identifier of the collection to delete.

        Returns:
            bool: True if deletion succeeded, False otherwise.
        """
        if collection_id in self._collections:
            del self._collections[collection_id]
            return True
        return False
    
    def get_prompts_by_collection(self, collection_id: str) -> List[Prompt]:
        """List prompts belonging to a specific collection.

        Args:
            collection_id (str): Collection identifier to filter prompts.

        Returns:
            List[Prompt]: Prompts assigned to the provided collection.
        """
        return [p for p in self._prompts.values() if p.collection_id == collection_id]
    
    # ============== Utility ==============
    
    def clear(self):
        """Reset the storage by clearing all prompts and collections.

        Returns:
            None
        """
        self._prompts.clear()
        self._collections.clear()


# Global storage instance
storage = Storage()
