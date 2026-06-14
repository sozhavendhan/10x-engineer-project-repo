"""TDD tests for Prompt Tags feature.

These tests are written BEFORE the implementation and will fail until
the tags feature is added to models, storage, utils, and api.

Run with: pytest tests/test_prompt_tags.py -v
"""

# ── Helpers ──────────────────────────────────────────────────────────────────

def _create_prompt(client, base_data, tags=None):
    """Create a prompt via POST and return the response JSON."""
    data = dict(base_data)
    if tags is not None:
        data["tags"] = tags
    r = client.post("/prompts", json=data)
    assert r.status_code == 201, r.text
    return r.json()


# ── Tags on Prompt Create ────────────────────────────────────────────────────

class TestPromptTagsOnCreate:
    """Tags are stored, normalized, and deduplicated when creating prompts."""

    def test_create_prompt_with_tags(self, client, sample_prompt_data):
        data = _create_prompt(client, sample_prompt_data, ["baseline", "customer-support"])
        assert "baseline" in data["tags"]
        assert "customer-support" in data["tags"]

    def test_tags_normalized_to_lowercase(self, client, sample_prompt_data):
        data = _create_prompt(client, sample_prompt_data, ["Baseline", "CUSTOMER-SUPPORT"])
        assert "baseline" in data["tags"]
        assert "customer-support" in data["tags"]
        assert "Baseline" not in data["tags"]
        assert "CUSTOMER-SUPPORT" not in data["tags"]

    def test_tags_are_deduplicated(self, client, sample_prompt_data):
        data = _create_prompt(client, sample_prompt_data, ["baseline", "Baseline", "BASELINE"])
        assert data["tags"].count("baseline") == 1

    def test_create_prompt_without_tags_defaults_to_empty_list(self, client, sample_prompt_data):
        data = _create_prompt(client, sample_prompt_data)
        assert data["tags"] == []

    def test_tag_name_too_long_returns_422(self, client, sample_prompt_data):
        payload = dict(sample_prompt_data)
        payload["tags"] = ["a" * 51]
        r = client.post("/prompts", json=payload)
        assert r.status_code == 422

    def test_empty_tag_name_returns_422(self, client, sample_prompt_data):
        payload = dict(sample_prompt_data)
        payload["tags"] = [""]
        r = client.post("/prompts", json=payload)
        assert r.status_code == 422

    def test_whitespace_only_tag_returns_422(self, client, sample_prompt_data):
        payload = dict(sample_prompt_data)
        payload["tags"] = ["   "]
        r = client.post("/prompts", json=payload)
        assert r.status_code == 422

    def test_more_than_20_tags_returns_422(self, client, sample_prompt_data):
        payload = dict(sample_prompt_data)
        payload["tags"] = [f"tag{i}" for i in range(21)]
        r = client.post("/prompts", json=payload)
        assert r.status_code == 422

    def test_exactly_20_tags_is_valid(self, client, sample_prompt_data):
        payload = dict(sample_prompt_data)
        payload["tags"] = [f"tag{i}" for i in range(20)]
        r = client.post("/prompts", json=payload)
        assert r.status_code == 201
        assert len(r.json()["tags"]) == 20

    def test_tags_field_present_in_response(self, client, sample_prompt_data):
        data = _create_prompt(client, sample_prompt_data)
        assert "tags" in data


# ── Tag Filtering on GET /prompts ────────────────────────────────────────────

class TestPromptTagFiltering:
    """GET /prompts?tags=... filters prompts using logical AND."""

    def test_filter_by_single_tag(self, client, sample_prompt_data):
        _create_prompt(client, sample_prompt_data, ["baseline"])
        _create_prompt(client, sample_prompt_data, ["experimental"])

        r = client.get("/prompts?tags=baseline")
        assert r.status_code == 200
        data = r.json()
        assert data["total"] == 1
        assert "baseline" in data["prompts"][0]["tags"]

    def test_filter_by_multiple_tags_uses_and_logic(self, client, sample_prompt_data):
        _create_prompt(client, sample_prompt_data, ["baseline", "executive"])
        _create_prompt(client, sample_prompt_data, ["baseline"])
        _create_prompt(client, sample_prompt_data, ["executive"])

        r = client.get("/prompts?tags=baseline,executive")
        assert r.status_code == 200
        data = r.json()
        assert data["total"] == 1
        assert "baseline" in data["prompts"][0]["tags"]
        assert "executive" in data["prompts"][0]["tags"]

    def test_filter_by_nonexistent_tag_returns_empty_list(self, client, sample_prompt_data):
        _create_prompt(client, sample_prompt_data, ["baseline"])

        r = client.get("/prompts?tags=nonexistent")
        assert r.status_code == 200
        assert r.json()["total"] == 0

    def test_tag_filter_is_case_insensitive(self, client, sample_prompt_data):
        _create_prompt(client, sample_prompt_data, ["baseline"])

        r = client.get("/prompts?tags=Baseline")
        assert r.status_code == 200
        assert r.json()["total"] == 1

    def test_tag_filter_combined_with_collection_filter(self, client, sample_prompt_data, sample_collection_data):
        col_r = client.post("/collections", json=sample_collection_data)
        col_id = col_r.json()["id"]

        _create_prompt(client, {**sample_prompt_data, "collection_id": col_id}, ["baseline"])
        _create_prompt(client, sample_prompt_data, ["baseline"])

        r = client.get(f"/prompts?tags=baseline&collection_id={col_id}")
        assert r.status_code == 200
        assert r.json()["total"] == 1

    def test_tag_filter_combined_with_search(self, client):
        client.post("/prompts", json={"title": "Sprint review", "content": "Content here", "tags": ["baseline"]})
        client.post("/prompts", json={"title": "Retro notes", "content": "Content here", "tags": ["baseline"]})

        r = client.get("/prompts?tags=baseline&search=sprint")
        assert r.status_code == 200
        assert r.json()["total"] == 1
        assert "sprint" in r.json()["prompts"][0]["title"].lower()

    def test_no_tag_filter_returns_all_prompts(self, client, sample_prompt_data):
        _create_prompt(client, sample_prompt_data, ["baseline"])
        _create_prompt(client, sample_prompt_data, ["experimental"])

        r = client.get("/prompts")
        assert r.status_code == 200
        assert r.json()["total"] == 2


# ── Tags on PUT and PATCH ────────────────────────────────────────────────────

class TestTagsOnUpdate:
    """Tags are updated correctly via PUT and PATCH."""

    def test_patch_replaces_tags(self, client, sample_prompt_data):
        prompt = _create_prompt(client, sample_prompt_data, ["original"])
        prompt_id = prompt["id"]

        r = client.patch(f"/prompts/{prompt_id}", json={"tags": ["updated"]})
        assert r.status_code == 200
        assert "updated" in r.json()["tags"]
        assert "original" not in r.json()["tags"]

    def test_patch_without_tags_leaves_tags_unchanged(self, client, sample_prompt_data):
        prompt = _create_prompt(client, sample_prompt_data, ["keep-me"])
        prompt_id = prompt["id"]

        r = client.patch(f"/prompts/{prompt_id}", json={"title": "New title"})
        assert r.status_code == 200
        assert "keep-me" in r.json()["tags"]

    def test_put_replaces_tags(self, client, sample_prompt_data):
        prompt = _create_prompt(client, sample_prompt_data, ["original"])
        prompt_id = prompt["id"]

        put_payload = dict(sample_prompt_data)
        put_payload["tags"] = ["replaced"]
        r = client.put(f"/prompts/{prompt_id}", json=put_payload)
        assert r.status_code == 200
        assert r.json()["tags"] == ["replaced"]
        assert "original" not in r.json()["tags"]

    def test_put_without_tags_defaults_to_empty(self, client, sample_prompt_data):
        prompt = _create_prompt(client, sample_prompt_data, ["original"])
        prompt_id = prompt["id"]

        r = client.put(f"/prompts/{prompt_id}", json=sample_prompt_data)
        assert r.status_code == 200
        assert r.json()["tags"] == []

    def test_patch_normalizes_tags(self, client, sample_prompt_data):
        prompt = _create_prompt(client, sample_prompt_data)
        r = client.patch(f"/prompts/{prompt['id']}", json={"tags": ["UPPER", "UPPER"]})
        assert r.status_code == 200
        assert r.json()["tags"] == ["upper"]


# ── Tag Catalog Endpoints ─────────────────────────────────────────────────────

class TestTagsCatalog:
    """Tests for GET /tags, POST /tags, and DELETE /tags/{tag}."""

    def test_get_tags_returns_empty_list_initially(self, client):
        r = client.get("/tags")
        assert r.status_code == 200
        data = r.json()
        assert "tags" in data
        assert data["tags"] == []

    def test_post_tag_creates_tag(self, client):
        r = client.post("/tags", json={"name": "experiment"})
        assert r.status_code == 201
        data = r.json()
        assert data["name"] == "experiment"

    def test_post_tag_normalizes_to_lowercase(self, client):
        r = client.post("/tags", json={"name": "Experiment"})
        assert r.status_code == 201
        assert r.json()["name"] == "experiment"

    def test_post_duplicate_tag_returns_200_with_existing(self, client):
        client.post("/tags", json={"name": "experiment"})
        r = client.post("/tags", json={"name": "experiment"})
        assert r.status_code == 200
        assert r.json()["name"] == "experiment"

    def test_post_tag_case_duplicate_returns_200(self, client):
        client.post("/tags", json={"name": "experiment"})
        r = client.post("/tags", json={"name": "EXPERIMENT"})
        assert r.status_code == 200

    def test_get_tags_shows_prompt_count(self, client, sample_prompt_data):
        _create_prompt(client, sample_prompt_data, ["experiment"])

        r = client.get("/tags")
        assert r.status_code == 200
        tags = r.json()["tags"]
        experiment_tag = next((t for t in tags if t["name"] == "experiment"), None)
        assert experiment_tag is not None
        assert experiment_tag["count"] == 1

    def test_get_tags_count_reflects_multiple_prompts(self, client, sample_prompt_data):
        _create_prompt(client, sample_prompt_data, ["experiment"])
        _create_prompt(client, sample_prompt_data, ["experiment"])

        r = client.get("/tags")
        tags = r.json()["tags"]
        experiment_tag = next(t for t in tags if t["name"] == "experiment")
        assert experiment_tag["count"] == 2

    def test_get_tags_sorted_alphabetically(self, client):
        client.post("/tags", json={"name": "zebra"})
        client.post("/tags", json={"name": "apple"})
        client.post("/tags", json={"name": "mango"})

        r = client.get("/tags")
        names = [t["name"] for t in r.json()["tags"]]
        assert names == sorted(names)

    def test_delete_tag_returns_204(self, client):
        client.post("/tags", json={"name": "experiment"})
        r = client.delete("/tags/experiment")
        assert r.status_code == 204

    def test_delete_tag_removes_from_catalog(self, client):
        client.post("/tags", json={"name": "experiment"})
        client.delete("/tags/experiment")

        r = client.get("/tags")
        names = [t["name"] for t in r.json()["tags"]]
        assert "experiment" not in names

    def test_delete_tag_disassociates_from_prompts(self, client, sample_prompt_data):
        prompt = _create_prompt(client, sample_prompt_data, ["experiment", "baseline"])
        prompt_id = prompt["id"]

        client.delete("/tags/experiment")

        prompt_r = client.get(f"/prompts/{prompt_id}")
        assert prompt_r.status_code == 200
        tags = prompt_r.json()["tags"]
        assert "experiment" not in tags
        assert "baseline" in tags

    def test_delete_nonexistent_tag_returns_404(self, client):
        r = client.delete("/tags/nonexistent")
        assert r.status_code == 404

    def test_creating_prompt_with_tags_adds_to_catalog(self, client, sample_prompt_data):
        _create_prompt(client, sample_prompt_data, ["auto-registered"])

        r = client.get("/tags")
        names = [t["name"] for t in r.json()["tags"]]
        assert "auto-registered" in names

    def test_prompt_tag_count_decrements_after_tag_removed_from_prompt(self, client, sample_prompt_data):
        prompt = _create_prompt(client, sample_prompt_data, ["experiment"])
        client.patch(f"/prompts/{prompt['id']}", json={"tags": []})

        r = client.get("/tags")
        tags = r.json()["tags"]
        experiment_tag = next((t for t in tags if t["name"] == "experiment"), None)
        # Tag entry still exists (was explicitly registered), count is now 0
        if experiment_tag is not None:
            assert experiment_tag["count"] == 0
