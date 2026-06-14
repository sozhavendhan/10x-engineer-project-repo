"""Storage tests for PromptLab."""

from app.models import Collection, Prompt
from app.storage import Storage


class TestPromptStorage:
    """Tests for prompt persistence operations."""

    def test_create_and_get_prompt(self):
        storage = Storage()
        prompt = Prompt(title="A", content="Body")

        created = storage.create_prompt(prompt)
        fetched = storage.get_prompt(prompt.id)

        assert created.id == prompt.id
        assert fetched is not None
        assert fetched.id == prompt.id

    def test_update_prompt(self):
        storage = Storage()
        prompt = Prompt(title="A", content="Body")
        storage.create_prompt(prompt)

        updated = Prompt(
            id=prompt.id,
            title="B",
            content="Updated",
            description="desc",
            collection_id=None,
            tags=["baseline"],
            created_at=prompt.created_at,
            updated_at=prompt.updated_at,
        )

        result = storage.update_prompt(prompt.id, updated)

        assert result is not None
        assert result.title == "B"
        assert result.tags == ["baseline"]

    def test_delete_prompt(self):
        storage = Storage()
        prompt = Prompt(title="A", content="Body")
        storage.create_prompt(prompt)

        assert storage.delete_prompt(prompt.id) is True
        assert storage.get_prompt(prompt.id) is None


class TestCollectionStorage:
    """Tests for collection persistence operations."""

    def test_create_and_get_collection(self):
        storage = Storage()
        collection = Collection(name="Dev")

        storage.create_collection(collection)
        fetched = storage.get_collection(collection.id)

        assert fetched is not None
        assert fetched.id == collection.id

    def test_get_prompts_by_collection(self):
        storage = Storage()
        collection = Collection(name="Dev")
        storage.create_collection(collection)

        p1 = Prompt(title="A", content="Body", collection_id=collection.id)
        p2 = Prompt(title="B", content="Body", collection_id=None)
        storage.create_prompt(p1)
        storage.create_prompt(p2)

        prompts = storage.get_prompts_by_collection(collection.id)

        assert len(prompts) == 1
        assert prompts[0].id == p1.id


class TestTagStorage:
    """Tests for tag catalog and usage operations."""

    def test_register_and_get_tag(self):
        storage = Storage()
        storage.register_tags(["baseline"])

        tag = storage.get_tag("baseline")

        assert tag is not None
        assert tag.name == "baseline"

    def test_get_all_tags_sorted(self):
        storage = Storage()
        storage.register_tags(["zeta", "alpha", "middle"])

        names = [tag.name for tag in storage.get_all_tags()]

        assert names == ["alpha", "middle", "zeta"]

    def test_delete_tag_disassociates_from_prompts(self):
        storage = Storage()
        storage.register_tags(["baseline", "keep"])

        prompt = Prompt(title="A", content="Body", tags=["baseline", "keep"])
        storage.create_prompt(prompt)

        deleted = storage.delete_tag("baseline")

        assert deleted is True
        fetched = storage.get_prompt(prompt.id)
        assert fetched is not None
        assert fetched.tags == ["keep"]

    def test_count_tag_usage(self):
        storage = Storage()
        storage.register_tags(["baseline"])
        storage.create_prompt(Prompt(title="A", content="Body", tags=["baseline"]))
        storage.create_prompt(Prompt(title="B", content="Body", tags=["baseline"]))

        assert storage.count_tag_usage("baseline") == 2

    def test_clear_resets_all_state(self):
        storage = Storage()
        storage.create_prompt(Prompt(title="A", content="Body"))
        storage.create_collection(Collection(name="Dev"))
        storage.register_tags(["baseline"])

        storage.clear()

        assert storage.get_all_prompts() == []
        assert storage.get_all_collections() == []
        assert storage.get_all_tags() == []
