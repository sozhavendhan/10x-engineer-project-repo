import { useEffect, useState } from "react";
import {
  createCollection,
  createPrompt,
  deletePrompt,
  getCollections,
  getPrompts,
  updatePrompt,
} from "./api";
import "./App.css";

const emptyPromptForm = {
  title: "",
  content: "",
  description: "",
  collection_id: "",
  tags: "",
};

function App() {
  const [prompts, setPrompts] = useState([]);
  const [collections, setCollections] = useState([]);
  const [promptForm, setPromptForm] = useState(emptyPromptForm);
  const [collectionForm, setCollectionForm] = useState({ name: "", description: "" });
  const [editingPromptId, setEditingPromptId] = useState(null);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  async function loadData() {
    try {
      setError("");
      const [promptData, collectionData] = await Promise.all([
        getPrompts(),
        getCollections(),
      ]);
      setPrompts(promptData);
      setCollections(collectionData);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  function handlePromptChange(event) {
    const { name, value } = event.target;
    setPromptForm((current) => ({ ...current, [name]: value }));
  }

  function handleCollectionChange(event) {
    const { name, value } = event.target;
    setCollectionForm((current) => ({ ...current, [name]: value }));
  }

  function buildPromptPayload() {
    return {
      title: promptForm.title,
      content: promptForm.content,
      description: promptForm.description || null,
      collection_id: promptForm.collection_id || null,
      tags: promptForm.tags
        ? promptForm.tags.split(",").map((tag) => tag.trim()).filter(Boolean)
        : [],
    };
  }

  async function handlePromptSubmit(event) {
    event.preventDefault();

    try {
      setError("");
      setMessage("");

      const payload = buildPromptPayload();

      if (editingPromptId) {
        await updatePrompt(editingPromptId, payload);
        setMessage("Prompt updated successfully.");
      } else {
        await createPrompt(payload);
        setMessage("Prompt created successfully.");
      }

      setPromptForm(emptyPromptForm);
      setEditingPromptId(null);
      await loadData();
    } catch (err) {
      setError(err.message);
    }
  }

  function startEdit(prompt) {
    setEditingPromptId(prompt.id);
    setPromptForm({
      title: prompt.title || "",
      content: prompt.content || "",
      description: prompt.description || "",
      collection_id: prompt.collection_id || "",
      tags: prompt.tags ? prompt.tags.join(", ") : "",
    });
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  async function handleDeletePrompt(id) {
    const confirmed = window.confirm("Delete this prompt?");
    if (!confirmed) return;

    try {
      setError("");
      setMessage("");
      await deletePrompt(id);
      setMessage("Prompt deleted successfully.");
      await loadData();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleCollectionSubmit(event) {
    event.preventDefault();

    try {
      setError("");
      setMessage("");
      await createCollection({
        name: collectionForm.name,
        description: collectionForm.description || null,
      });
      setCollectionForm({ name: "", description: "" });
      setMessage("Collection created successfully.");
      await loadData();
    } catch (err) {
      setError(err.message);
    }
  }

  function getCollectionName(collectionId) {
    const collection = collections.find((item) => item.id === collectionId);
    return collection ? collection.name : "No collection";
  }

  return (
    <div className="app">
      <header className="hero">
        <div>
          <p className="eyebrow">PromptLab</p>
          <h1>Prompt Engineering Workspace</h1>
          <p>
            Create, organize, edit, and manage prompts from a React frontend connected to the FastAPI backend.
          </p>
        </div>
      </header>

      {message && <div className="alert success">{message}</div>}
      {error && <div className="alert error">{error}</div>}

      <main className="layout">
        <section className="card">
          <h2>{editingPromptId ? "Edit Prompt" : "Create Prompt"}</h2>

          <form onSubmit={handlePromptSubmit} className="form">
            <label>
              Title
              <input
                name="title"
                value={promptForm.title}
                onChange={handlePromptChange}
                required
              />
            </label>

            <label>
              Content
              <textarea
                name="content"
                value={promptForm.content}
                onChange={handlePromptChange}
                rows="6"
                required
              />
            </label>

            <label>
              Description
              <input
                name="description"
                value={promptForm.description}
                onChange={handlePromptChange}
              />
            </label>

            <label>
              Collection
              <select
                name="collection_id"
                value={promptForm.collection_id}
                onChange={handlePromptChange}
              >
                <option value="">No collection</option>
                {collections.map((collection) => (
                  <option key={collection.id} value={collection.id}>
                    {collection.name}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Tags comma separated
              <input
                name="tags"
                value={promptForm.tags}
                onChange={handlePromptChange}
                placeholder="marketing, ai, summary"
              />
            </label>

            <div className="button-row">
              <button type="submit">
                {editingPromptId ? "Update Prompt" : "Create Prompt"}
              </button>

              {editingPromptId && (
                <button
                  type="button"
                  className="secondary"
                  onClick={() => {
                    setEditingPromptId(null);
                    setPromptForm(emptyPromptForm);
                  }}
                >
                  Cancel Edit
                </button>
              )}
            </div>
          </form>
        </section>

        <section className="card">
          <h2>Create Collection</h2>

          <form onSubmit={handleCollectionSubmit} className="form">
            <label>
              Name
              <input
                name="name"
                value={collectionForm.name}
                onChange={handleCollectionChange}
                required
              />
            </label>

            <label>
              Description
              <input
                name="description"
                value={collectionForm.description}
                onChange={handleCollectionChange}
              />
            </label>

            <button type="submit">Create Collection</button>
          </form>

          <div className="collection-list">
            <h3>Collections</h3>
            {collections.length === 0 ? (
              <p className="muted">No collections yet.</p>
            ) : (
              collections.map((collection) => (
                <div key={collection.id} className="collection-item">
                  <strong>{collection.name}</strong>
                  <span>{collection.description || "No description"}</span>
                </div>
              ))
            )}
          </div>
        </section>
      </main>

      <section className="card full-width">
        <div className="section-heading">
          <div>
            <h2>Prompt List</h2>
            <p className="muted">{prompts.length} prompt(s) available</p>
          </div>
          <button className="secondary" onClick={loadData}>
            Refresh
          </button>
        </div>

        {prompts.length === 0 ? (
          <p className="muted">No prompts found. Create your first prompt above.</p>
        ) : (
          <div className="prompt-grid">
            {prompts.map((prompt) => (
              <article key={prompt.id} className="prompt-card">
                <div className="prompt-card-header">
                  <h3>{prompt.title}</h3>
                  <span>{getCollectionName(prompt.collection_id)}</span>
                </div>

                <p className="description">
                  {prompt.description || "No description provided."}
                </p>

                <pre>{prompt.content}</pre>

                {prompt.tags && prompt.tags.length > 0 && (
                  <div className="tags">
                    {prompt.tags.map((tag) => (
                      <span key={tag}>{tag}</span>
                    ))}
                  </div>
                )}

                <div className="prompt-actions">
                  <button className="secondary" onClick={() => startEdit(prompt)}>
                    Edit
                  </button>
                  <button className="danger" onClick={() => handleDeletePrompt(prompt.id)}>
                    Delete
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default App;