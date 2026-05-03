"""FastAPI routes for PromptLab"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional



from app.models import (
    Prompt,
    PromptCreate,
    PromptUpdate,
    PromptPatch,
    Collection,
    CollectionCreate,
    PromptList,
    CollectionList,
    HealthResponse,
    get_current_time
)



from app.storage import storage
from app.utils import sort_prompts_by_date, filter_prompts_by_collection, search_prompts
from app import __version__


app = FastAPI(
    title="PromptLab API",
    description="AI Prompt Engineering Platform",
    version=__version__
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============== Health Check ==============

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Return the current health state and version of the API.

    Returns:
        HealthResponse: Service health and version metadata.
    """
    return HealthResponse(status="healthy", version=__version__)


# ============== Prompt Endpoints ==============

@app.get("/prompts", response_model=PromptList)
def list_prompts(
    collection_id: Optional[str] = None,
    search: Optional[str] = None
):
    """Return prompts optionally filtered by collection or search term.

    Args:
        collection_id (Optional[str]): Only include prompts in this collection.
        search (Optional[str]): Case-insensitive search term for titles or descriptions.

    Returns:
        PromptList: Matched prompts sorted newest first.
    """

    prompts = storage.get_all_prompts()
    
    # Filter by collection if specified
    if collection_id:
        prompts = filter_prompts_by_collection(prompts, collection_id)
    
    # Search if query provided
    if search:
        prompts = search_prompts(prompts, search)
    
    # Sort by date (newest first)
    prompts = sort_prompts_by_date(prompts, descending=True)
    
    return PromptList(prompts=prompts, total=len(prompts))


@app.get("/prompts/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str):
    """Retrieve a single prompt by its unique identifier.

    Args:
        prompt_id (str): Identifier for the prompt to fetch.

    Returns:
        Prompt: Prompt matching the provided identifier.

    Raises:
        HTTPException: If the prompt does not exist.
    """

    prompt = storage.get_prompt(prompt_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    return prompt

@app.post("/prompts", response_model=Prompt, status_code=201)
def create_prompt(prompt_data: PromptCreate):
    """Create a new prompt record.

    Args:
        prompt_data (PromptCreate): Payload describing the prompt to persist.

    Returns:
        Prompt: The newly created prompt, including generated metadata.

    Raises:
        HTTPException: If the referenced collection cannot be found.
    """

    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    prompt = Prompt(**prompt_data.model_dump())
    return storage.create_prompt(prompt)


@app.put("/prompts/{prompt_id}", response_model=Prompt)
def update_prompt(prompt_id: str, prompt_data: PromptUpdate):
    """Replace an entire prompt record with the provided payload.

    Args:
        prompt_id (str): Identifier of the prompt to update.
        prompt_data (PromptUpdate): Replacement data for the prompt.

    Returns:
        Prompt: The updated prompt with refreshed metadata.

    Raises:
        HTTPException: If the prompt or target collection cannot be found.
    """

    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    if prompt_data.collection_id:
        collection = storage.get_collection(prompt_data.collection_id)
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")
    
    updated_prompt = Prompt(
        id=existing.id,
        title=prompt_data.title,
        content=prompt_data.content,
        description=prompt_data.description,
        collection_id=prompt_data.collection_id,
        created_at=existing.created_at,
        updated_at=get_current_time()
    )
    
    return storage.update_prompt(prompt_id, updated_prompt)


@app.patch("/prompts/{prompt_id}", response_model=Prompt)
def patch_prompt(prompt_id: str, prompt_data: PromptPatch):
    """Apply a partial update to a prompt record.

    Args:
        prompt_id (str): Identifier of the prompt to patch.
        prompt_data (PromptPatch): Fields to update on the prompt.

    Returns:
        Prompt: The prompt after applying the partial update.

    Raises:
        HTTPException: If the prompt or referenced collection does not exist.
    """

    existing = storage.get_prompt(prompt_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Prompt not found")

    updates = prompt_data.model_dump(exclude_unset=True)

    if "collection_id" in updates and updates["collection_id"]:
        collection = storage.get_collection(updates["collection_id"])
        if not collection:
            raise HTTPException(status_code=400, detail="Collection not found")

    updated_prompt = Prompt(
        id=existing.id,
        title=updates.get("title", existing.title),
        content=updates.get("content", existing.content),
        description=updates.get("description", existing.description),
        collection_id=updates.get("collection_id", existing.collection_id),
        created_at=existing.created_at,
        updated_at=get_current_time()
    )

    return storage.update_prompt(prompt_id, updated_prompt)

@app.delete("/prompts/{prompt_id}", status_code=204)
def delete_prompt(prompt_id: str):
    """Hard delete a prompt from the in-memory store.

    Args:
        prompt_id (str): Identifier of the prompt to delete.

    Returns:
        None

    Raises:
        HTTPException: If the prompt cannot be found.
    """

    if not storage.delete_prompt(prompt_id):
        raise HTTPException(status_code=404, detail="Prompt not found")
    return None


# ============== Collection Endpoints ==============

@app.get("/collections", response_model=CollectionList)
def list_collections():
    """Return all defined collections.

    Returns:
        CollectionList: All collections currently persisted.
    """

    collections = storage.get_all_collections()
    return CollectionList(collections=collections, total=len(collections))


@app.get("/collections/{collection_id}", response_model=Collection)
def get_collection(collection_id: str):
    """Retrieve a single collection by its identifier.

    Args:
        collection_id (str): Identifier of the desired collection.

    Returns:
        Collection: The matching collection record.

    Raises:
        HTTPException: If the collection cannot be found.
    """

    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@app.post("/collections", response_model=Collection, status_code=201)
def create_collection(collection_data: CollectionCreate):
    """Persist a new collection record.

    Args:
        collection_data (CollectionCreate): Attributes for the new collection.

    Returns:
        Collection: The collection record with generated id and timestamps.
    """

    collection = Collection(**collection_data.model_dump())
    return storage.create_collection(collection)


@app.delete("/collections/{collection_id}", status_code=204)
def delete_collection(collection_id: str):
    """Delete a collection and orphan any prompts assigned to it.

    Args:
        collection_id (str): Identifier of the collection to remove.

    Returns:
        None

    Raises:
        HTTPException: If the collection cannot be found.
    """

    collection = storage.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    prompts_in_collection = storage.get_prompts_by_collection(collection_id)

    for prompt in prompts_in_collection:
        updated_prompt = Prompt(
            id=prompt.id,
            title=prompt.title,
            content=prompt.content,
            description=prompt.description,
            collection_id=None,
            created_at=prompt.created_at,
            updated_at=get_current_time(),
        )
        storage.update_prompt(prompt.id, updated_prompt)

    storage.delete_collection(collection_id)
    return None
