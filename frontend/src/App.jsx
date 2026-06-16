import { useEffect, useState } from "react";
import {
  createCollection,
  createPrompt,
  deletePrompt,
  deleteCollection,
  getCollections,
  getPrompts,
  updatePrompt,
} from "./api";
import {
  Layout,
  PromptForm,
  CollectionForm,
  CollectionList,
  PromptList,
  SearchBar,
  LoadingSpinner,
  PromptDetail,
} from "./components";
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
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState("");
  const [selectedCollectionFilter, setSelectedCollectionFilter] = useState(null);
  const [selectedPromptDetail, setSelectedPromptDetail] = useState(null);

  async function loadData() {
    try {
      setError("");
      setLoading(true);
      const [promptData, collectionData] = await Promise.all([
        getPrompts(),
        getCollections(),
      ]);
      setPrompts(promptData);
      setCollections(collectionData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
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

  function getFilteredPrompts() {
    return prompts.filter((prompt) => {
      const matchesSearch =
        prompt.title.toLowerCase().includes(searchText.toLowerCase()) ||
        prompt.content.toLowerCase().includes(searchText.toLowerCase()) ||
        (prompt.description && prompt.description.toLowerCase().includes(searchText.toLowerCase()));

      const matchesCollection =
        selectedCollectionFilter === null || prompt.collection_id === selectedCollectionFilter;

      return matchesSearch && matchesCollection;
    });
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

  async function handleDeleteCollection(id) {
    const confirmed = window.confirm("Delete this collection? Prompts will not be deleted.");
    if (!confirmed) return;

    try {
      setError("");
      setMessage("");
      await deleteCollection(id);
      setMessage("Collection deleted successfully.");
      await loadData();
    } catch (err) {
      setError(err.message);
    }
  }

  function handleViewPromptDetail(prompt) {
    setSelectedPromptDetail(prompt);
  }

  function getCollectionName(collectionId) {
    const collection = collections.find((item) => item.id === collectionId);
    return collection ? collection.name : "No collection";
  }

  return (
    <Layout message={message} error={error}>
      <LoadingSpinner isLoading={loading} message="Loading data..." />

      <main className="layout">
        <PromptForm
          promptForm={promptForm}
          collections={collections}
          isEditing={!!editingPromptId}
          onSubmit={handlePromptSubmit}
          onChange={handlePromptChange}
          onCancel={() => {
            setEditingPromptId(null);
            setPromptForm(emptyPromptForm);
          }}
        />

        <div className="card">
          <h3>Search & Filter</h3>
          <SearchBar
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            placeholder="Search prompts by title, content, or description..."
          />

          <h3 style={{ marginTop: "1.5rem" }}>Filter by Collection</h3>
          <button
            className={selectedCollectionFilter === null ? "secondary active" : "secondary"}
            onClick={() => setSelectedCollectionFilter(null)}
            style={{ marginBottom: "0.5rem", marginRight: "0.5rem" }}
          >
            All Prompts
          </button>
          {collections.map((collection) => (
            <button
              key={collection.id}
              className={selectedCollectionFilter === collection.id ? "secondary active" : "secondary"}
              onClick={() => setSelectedCollectionFilter(collection.id)}
              style={{ marginBottom: "0.5rem", marginRight: "0.5rem" }}
            >
              {collection.name}
            </button>
          ))}
        </div>

        <div className="card">
          <CollectionForm
            collectionForm={collectionForm}
            onChange={handleCollectionChange}
            onSubmit={handleCollectionSubmit}
          />
          <CollectionList
            collections={collections}
            onDelete={handleDeleteCollection}
          />
        </div>
      </main>

      <PromptList
        prompts={getFilteredPrompts()}
        collections={collections}
        onEdit={startEdit}
        onDelete={handleDeletePrompt}
        onView={handleViewPromptDetail}
        onRefresh={loadData}
      />

      {selectedPromptDetail && (
        <div className="card full-width">
          <button
            className="secondary"
            onClick={() => setSelectedPromptDetail(null)}
            style={{ marginBottom: "1rem" }}
          >
            ✕ Close Details
          </button>
          <PromptDetail
            prompt={selectedPromptDetail}
            collectionName={getCollectionName(selectedPromptDetail.collection_id)}
          />
        </div>
      )}
    </Layout>
  );
}

export default App;