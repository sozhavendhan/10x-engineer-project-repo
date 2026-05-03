"""Pydantic models for PromptLab"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4


def generate_id() -> str:
    """Generate a random UUID for new records.

    Returns:
        str: A string representation of a newly generated UUID4.
    """
    return str(uuid4())


def get_current_time() -> datetime:
    """Return the current UTC timestamp used for auditing.

    Returns:
        datetime: Current UTC datetime.
    """
    return datetime.utcnow()


# ============== Prompt Models ==============

class PromptBase(BaseModel):
    """Shared fields for prompt creation, replacement, and presentation.

    Args:
        title (str): A descriptive title for the prompt (1-200 characters).
        content (str): The prompt template body containing optional variables.
        description (Optional[str]): Optional free-text description (up to 500 characters).
        collection_id (Optional[str]): Optional reference to an existing collection.
    """

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class PromptCreate(PromptBase):
    """Schema required when creating a new prompt."""


class PromptUpdate(PromptBase):
    """Schema used when replacing an existing prompt via PUT."""


class PromptPatch(BaseModel):
    """Schema that allows partial updates when patching a prompt.

    Args:
        title (Optional[str]): Optional new title for the prompt.
        content (Optional[str]): Optional new prompt body.
        description (Optional[str]): Optional new description.
        collection_id (Optional[str]): Optional new collection assignment.
    """

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, max_length=500)
    collection_id: Optional[str] = None


class Prompt(PromptBase):
    """Response schema for a fully populated prompt record.

    Args:
        id (str): Unique identifier for the prompt.
        created_at (datetime): Timestamp when the prompt was created.
        updated_at (datetime): Timestamp for the most recent update.
    """

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)
    updated_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Collection Models ==============

class CollectionBase(BaseModel):
    """Shared fields for collection creation and presentation.

    Args:
        name (str): Human-friendly name for the collection (1-100 characters).
        description (Optional[str]): Optional description for the collection (up to 500 characters).
    """

    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionCreate(CollectionBase):
    """Schema required when creating a new collection."""


class Collection(CollectionBase):
    """Response schema for a collection record.

    Args:
        id (str): Unique identifier for the collection.
        created_at (datetime): Timestamp when the collection was created.
    """

    id: str = Field(default_factory=generate_id)
    created_at: datetime = Field(default_factory=get_current_time)

    class Config:
        from_attributes = True


# ============== Response Models ==============

class PromptList(BaseModel):
    """Response payload for listing prompts.

    Args:
        prompts (List[Prompt]): Prompts that match the request criteria.
        total (int): Total number of prompts returned.
    """

    prompts: List[Prompt]
    total: int


class CollectionList(BaseModel):
    """Response payload for listing collections.

    Args:
        collections (List[Collection]): Collections returned by the request.
        total (int): Total number of collections returned.
    """

    collections: List[Collection]
    total: int


class HealthResponse(BaseModel):
    """Shape of the health-check response.

    Args:
        status (str): Service health indicator (e.g., "healthy").
        version (str): Current service version derived from the package.
    """

    status: str
    version: str
