"""Utility tests for PromptLab."""

from datetime import datetime, timedelta

from app.models import Prompt
from app.utils import (
    extract_variables,
    filter_prompts_by_collection,
    filter_prompts_by_tags,
    search_prompts,
    sort_prompts_by_date,
    validate_prompt_content,
)


def _make_prompt(title: str, content: str, minutes_offset: int = 0, **kwargs):
    """Create a prompt with deterministic timestamps for sorting tests."""
    base = datetime(2026, 1, 1, 12, 0, 0)
    ts = base + timedelta(minutes=minutes_offset)
    return Prompt(title=title, content=content, created_at=ts, updated_at=ts, **kwargs)


class TestSortPrompts:
    """Tests for prompt sorting helper."""

    def test_sort_prompts_descending(self):
        p1 = _make_prompt("older", "A", minutes_offset=0)
        p2 = _make_prompt("newer", "B", minutes_offset=10)

        sorted_prompts = sort_prompts_by_date([p1, p2], descending=True)

        assert [p.title for p in sorted_prompts] == ["newer", "older"]

    def test_sort_prompts_ascending(self):
        p1 = _make_prompt("older", "A", minutes_offset=0)
        p2 = _make_prompt("newer", "B", minutes_offset=10)

        sorted_prompts = sort_prompts_by_date([p1, p2], descending=False)

        assert [p.title for p in sorted_prompts] == ["older", "newer"]


class TestFilterPrompts:
    """Tests for filtering and searching helpers."""

    def test_filter_prompts_by_collection(self):
        p1 = _make_prompt("a", "A", collection_id="c1")
        p2 = _make_prompt("b", "B", collection_id="c2")

        results = filter_prompts_by_collection([p1, p2], "c1")

        assert len(results) == 1
        assert results[0].title == "a"

    def test_search_prompts_matches_title_or_description(self):
        p1 = _make_prompt("Release Summary", "A", description="weekly rollup")
        p2 = _make_prompt("Other", "B", description="engineering")

        title_match = search_prompts([p1, p2], "release")
        description_match = search_prompts([p1, p2], "weekly")

        assert len(title_match) == 1
        assert title_match[0].title == "Release Summary"
        assert len(description_match) == 1
        assert description_match[0].title == "Release Summary"

    def test_filter_prompts_by_tags_uses_and_logic(self):
        p1 = _make_prompt("a", "A", tags=["baseline", "executive"])
        p2 = _make_prompt("b", "B", tags=["baseline"])
        p3 = _make_prompt("c", "C", tags=["executive"])

        results = filter_prompts_by_tags([p1, p2, p3], ["baseline", "executive"])

        assert len(results) == 1
        assert results[0].title == "a"

    def test_filter_prompts_by_tags_empty_filter_returns_all(self):
        prompts = [_make_prompt("a", "A"), _make_prompt("b", "B")]

        results = filter_prompts_by_tags(prompts, [])

        assert len(results) == 2


class TestPromptContentHelpers:
    """Tests for content validation and variable extraction helpers."""

    def test_validate_prompt_content(self):
        assert validate_prompt_content("valid content") is True
        assert validate_prompt_content("  too  ") is False
        assert validate_prompt_content("   ") is False
        assert validate_prompt_content("") is False

    def test_extract_variables(self):
        text = "Summarize {{input}} for {{audience}} with {{tone}}"

        variables = extract_variables(text)

        assert variables == ["input", "audience", "tone"]
