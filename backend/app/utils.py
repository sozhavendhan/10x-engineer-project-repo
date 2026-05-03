"""Utility functions for PromptLab"""

from typing import List
from app.models import Prompt


def sort_prompts_by_date(prompts: List[Prompt], descending: bool = True) -> List[Prompt]:
    """Sort prompts by their creation timestamp.

    Args:
        prompts (List[Prompt]): Prompts to order.
        descending (bool): If True, newest prompts appear first.

    Returns:
        List[Prompt]: Prompts ordered by creation date.
    """
    return sorted(prompts, key=lambda p: p.created_at, reverse=descending)


def filter_prompts_by_collection(prompts: List[Prompt], collection_id: str) -> List[Prompt]:
    """Return prompts that belong to a single collection.

    Args:
        prompts (List[Prompt]): Prompts to filter.
        collection_id (str): Collection identifier to match.

    Returns:
        List[Prompt]: Prompts assigned to the provided collection.
    """
    return [p for p in prompts if p.collection_id == collection_id]


def search_prompts(prompts: List[Prompt], query: str) -> List[Prompt]:
    """Filter prompts using a case-insensitive text query.

    Args:
        prompts (List[Prompt]): Prompts to search.
        query (str): Text to search for in titles and descriptions.

    Returns:
        List[Prompt]: Prompts containing the query.
    """
    query_lower = query.lower()
    return [
        p for p in prompts 
        if query_lower in p.title.lower() or 
           (p.description and query_lower in p.description.lower())
    ]


def validate_prompt_content(content: str) -> bool:
    """Validate that a prompt body meets minimum length expectations.

    Args:
        content (str): Prompt text to validate.

    Returns:
        bool: True if the prompt is not empty, not whitespace, and at least 10 characters.
    """
    if not content or not content.strip():
        return False
    return len(content.strip()) >= 10


def extract_variables(content: str) -> List[str]:
    """Extract all template variables enclosed in double curly braces.

    Args:
        content (str): Prompt text containing template variables.

    Returns:
        List[str]: Ordered list of unique variable names.
    """
    import re
    pattern = r'\{\{(\w+)\}\}'
    return re.findall(pattern, content)

