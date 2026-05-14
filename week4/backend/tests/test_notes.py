def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_add_tags_to_note_happy_path(client):
    # Create a note first
    r = client.post("/notes/", json={"title": "Tagged Note", "content": "Some content"})
    assert r.status_code == 201, r.text
    note_id = r.json()["id"]

    # Add tags to the note
    r = client.post(f"/notes/{note_id}/tags", json={"tags": ["python", "fastapi"]})
    assert r.status_code == 200, r.text
    data = r.json()

    # Response should include the note fields plus the tags list
    assert data["id"] == note_id
    assert data["title"] == "Tagged Note"
    assert data["content"] == "Some content"
    assert isinstance(data["tags"], list)
    assert sorted(data["tags"]) == ["fastapi", "python"]


def test_add_tags_to_nonexistent_note_returns_404(client):
    # Posting tags to a note ID that does not exist should return 404
    r = client.post("/notes/99999/tags", json={"tags": ["orphan"]})
    assert r.status_code == 404, r.text


def test_add_tags_twice_accumulates_tags(client):
    # Tags added in a second POST should be merged with the first set (additive behavior)
    r = client.post("/notes/", json={"title": "Accumulate Tags", "content": "content"})
    assert r.status_code == 201, r.text
    note_id = r.json()["id"]

    # First tag POST
    r = client.post(f"/notes/{note_id}/tags", json={"tags": ["alpha"]})
    assert r.status_code == 200, r.text

    # Second tag POST with a different tag
    r = client.post(f"/notes/{note_id}/tags", json={"tags": ["beta"]})
    assert r.status_code == 200, r.text
    data = r.json()

    # Both tags should be present
    assert "alpha" in data["tags"]
    assert "beta" in data["tags"]


def test_add_empty_tag_list(client):
    # Posting an empty tags list to an existing note should return 200 with an empty tags list
    r = client.post("/notes/", json={"title": "No Tags", "content": "plain"})
    assert r.status_code == 201, r.text
    note_id = r.json()["id"]

    r = client.post(f"/notes/{note_id}/tags", json={"tags": []})
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["tags"] == []
