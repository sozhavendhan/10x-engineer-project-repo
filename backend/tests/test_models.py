"""Model tests for PromptLab."""

import pytest
from pydantic import ValidationError

from app.models import PromptCreate, PromptPatch, TagCreate


class TestPromptTagValidation:
    """Tests for prompt tag validation and normalization."""

    def test_prompt_create_defaults_tags_to_empty_list(self):
        model = PromptCreate(title="t", content="c")
        assert model.tags == []

    def test_prompt_create_normalizes_and_deduplicates_tags(self):
        model = PromptCreate(
            title="t",
            content="c",
            tags=["Baseline", "baseline", "EXPERIMENT"],
        )
        assert model.tags == ["baseline", "experiment"]

    def test_prompt_create_rejects_whitespace_tag(self):
        with pytest.raises(ValidationError):
            PromptCreate(title="t", content="c", tags=["   "])

    def test_prompt_create_rejects_too_many_tags(self):
        with pytest.raises(ValidationError):
            PromptCreate(
                title="t",
                content="c",
                tags=[f"tag{i}" for i in range(21)],
            )

    def test_prompt_patch_keeps_none(self):
        model = PromptPatch()
        assert model.tags is None

    def test_prompt_patch_normalizes_tags(self):
        model = PromptPatch(tags=["UPPER", "upper", "Mixed"])
        assert model.tags == ["upper", "mixed"]


class TestTagCreate:
    """Tests for tag creation schema."""

    def test_tag_create_lowercases_name(self):
        model = TagCreate(name="Experiment")
        assert model.name == "experiment"

    def test_tag_create_trims_whitespace(self):
        model = TagCreate(name="  baseline  ")
        assert model.name == "baseline"

    def test_tag_create_rejects_whitespace_only(self):
        with pytest.raises(ValidationError):
            TagCreate(name="   ")
